from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import login
from django_redis import get_redis_connection
import json, re
from QQLoginTool.QQtool import OAuthQQ
from .models import OAuthQQUser
from users.models import User
from meiduo_mall.utils.secret import SecretOauth
from carts.utils import merge_cart_cookie_to_redis


# QQ登陆接口1
class QQURLView(View):

    def get(self, request):
        # 1、提取参数
        next = request.GET.get('next')
        # 2、校验参数
        # 3、业务数据处理 —— 获取登陆页面url
        oauth = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI,
            state=next
        )
        login_url = oauth.get_qq_url()

        # 4、构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'login_url': login_url
        })


class QQUserView(View):

    # QQ登陆接口2
    def get(self, request):
        # 1、提取参数
        code = request.GET.get('code')
        # 2、校验参数
        if code is None:
            return JsonResponse({'code': 400, 'errmsg': '缺少必要参数'})

        # 3、业务数据处理(业务性校验) —— 获取openid
        # TODO: 获取用户qq身份(openid)
        # 3.1、获取OAuthQQ对象
        oauth = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI,
            state='/'
        )
        try:
            # 3.2、校验code，获取Access Token
            access_token = oauth.get_access_token(code)
            # 3.3、根据Access Token获取openid
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': 'qq身份验证有误！'})

        # TODO: 判断用户是否绑定账号
        try:
            oauth_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist as e:
            # 未绑定 —— 加密openid返回给前端(前端跳转到绑定页面)
            access_token = SecretOauth().dumps({'openid': openid})
            return JsonResponse({'code': 400, 'errmsg': 'ok', 'access_token': access_token})
        else:
            # 已经绑定 —— 直接正常响应 —— 登陆成功
            user = oauth_user.user  # OAuthQQUser的user属性是一个外间关联字段，关联的User模型类对象
            # 状态保持
            login(request, user)
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            # 设置cookie中的username做页面展示
            response.set_cookie('username', user.username, max_age=14 * 3600 * 24)
            # TODO: 合并购物车
            merge_cart_cookie_to_redis(request, response)
            return response

    # QQ登陆接口3
    def post(self, request):
        # 1、提取参数
        data = json.loads(request.body.decode())
        mobile = data.get('mobile')
        password = data.get('password')
        sms_code = data.get('sms_code')
        access_token = data.get('access_token')  # 加密的{"openid": "123456789"}

        # 2、校验参数
        # 2.1、必要性校验
        if not all([mobile, password, sms_code, access_token]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必要参数'})
        # 2.2、约束性校验
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '手机号格式有误'})
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': '密码格式有误'})
        # 2.3、业务性校验
        conn = get_redis_connection('verify_code')
        sms_code_from_redis = conn.get('sms_%s' % mobile)
        if not sms_code_from_redis:
            return JsonResponse({'code': 400, 'errmsg': '短信验证码过期'})
        if sms_code != sms_code_from_redis.decode():
            return JsonResponse({'code': 400, 'errmsg': '短信验证码输入错误'})

        # 3、业务数据处理 —— 绑定账号
        # 3.1、解密openid
        data_dict = SecretOauth().loads(access_token)  # {"openid": "1234567890"} or None
        if not data_dict:
            return JsonResponse({'code': 400, 'errmsg': 'openid有误！'})
        openid = data_dict.get('openid')
        # 3.2、根据用户传递的手机号查找用户对象
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist as e:
            # 未注册美多账号  —— 新建绑定
            user = User.objects.create_user(
                username=mobile,
                mobile=mobile,
                password=password
            )
        else:
            # 注册过美多账号  —— 直接绑定
            if not user.check_password(password):
                return JsonResponse({'code': 400, 'errmsg': '密码错误'})

        # 绑定
        OAuthQQUser.objects.create(
            user=user,
            openid=openid
        )

        # 4、构建响应
        login(request, user)
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)
        # TODO: 合并购物车
        merge_cart_cookie_to_redis(request, response)
        return response
