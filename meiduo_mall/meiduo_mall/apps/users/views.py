from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import login
from django_redis import get_redis_connection
from .models import User

import logging, re, json

logger = logging.getLogger('django')


# Create your views here.

# 判断用户名重复注册接口
class UsernameCountView(View):

    # 由于接口定义的请求方式是GET，所以映射的视图方法是self.get()
    # 所以我们需要定义self.get()视图方法
    def get(self, request, username):
        # 1、提取参数
        # username是路径参数，在路由匹配的时候通过正则或者转化器提取传递到视图函数中。
        # 2、校验参数
        # 路径参数正则匹配或转化器匹配，已经起到了校验的作用。
        # 3、数据处理 —— 根据username统计用户数量
        try:
            count = User.objects.filter(
                username=username
            ).count()
        except Exception as e:
            # 记录日志
            logger.info("数据库访问失败！")
            # 构建错误响应
            return JsonResponse({
                "code": 400,
                "errmsg": "数据库错误"
            })

        # 4、构建响应
        return JsonResponse({
            "code": 0,
            "errmsg": "ok",
            "count": count
        })


# 判断手机号重复注册
class MobileCountView(View):

    def get(self, request, mobile):
        # 1、提取参数
        # 2、校验参数
        # 3、业务数据处理 —— 根据手机号统计注册用户数量
        try:
            count = User.objects.filter(
                mobile=mobile
            ).count()
        except Exception as e:
            # 记录日志
            logger.info("数据库访问失败！")
            # 构建错误响应
            return JsonResponse({
                "code": 400,
                "errmsg": "数据库错误"
            })
        # 4、构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'count': count
        })


# 用户注册接口
class RegisterView(View):

    def post(self, request):
        # 1、提取参数
        # request.body --> b"{'username': 'weiwei'....}"
        json_str = request.body.decode()  # "{'username': 'weiwei'....}"
        data = json.loads(json_str)  # {'username': 'weiwei'....}

        # 必传
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        mobile = data.get('mobile')
        sms_code = data.get('sms_code')
        # 非必传
        allow = data.get('allow', False)

        # 2、校验参数
        # 2.1、必要性校验
        # 当且仅当username、password、password2、mobile和sms_code都不为None，表示都传了
        if not all([username, password, password2, mobile, sms_code]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必要参数'
            })

        # 2.2、约束性校验
        if not allow:
            return JsonResponse({
                'code': 400,
                'errmsg': '请勾选同意用户协议'
            })
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return JsonResponse({
                'code': 400,
                'errmsg': '用户名格式有误'
            })
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({
                'code': 400,
                'errmsg': '手机号格式有误'
            })
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return JsonResponse({
                'code': 400,
                'errmsg': '密码格式有误'
            })
        if password != password2:
            return JsonResponse({
                'code': 400,
                'errmsg': '密码输入不一致'
            })

        # 2.3、业务性校验 —— 短信验证码等。
        # TODO: 此处将来填充校验短信验证码逻辑代码
        conn = get_redis_connection('verify_code')
        # (1)、读取redis中记录的手机短信验证码
        sms_code_from_redis = conn.get('sms_%s' % mobile)  # b'123456' or None
        # (2)、判断是否过期
        if not sms_code_from_redis:
            return JsonResponse({'code': 400, 'errmsg': '短信验证码失效'})
        # (3)、判断和用户输入的是否一致
        if sms_code_from_redis.decode() != sms_code:
            return JsonResponse({'code': 400, 'errmsg': '短信验证码输入有误'})
        # 3、业务数据处理 —— 新建用户模型类对象保存数据库，用户状态保持。
        try:
            # User.objects.create() --> 密码未加密
            # User.objects.create_user() --> 密码加密。AbstractUser提供都方法
            # User.objects.create_superuser() --> 密码加密,超级管理员。要求必传email。AbstractUser提供都方法
            # 此处项目一新建的是普通用户，所以只需使用create_user
            user = User.objects.create_user(
                username=username,
                password=password,
                mobile=mobile
            )
        except Exception as e:
            print(e)
            logger.error('注册用户，写入mysql失败！')
            return JsonResponse({
                'code': 400,
                'errmsg': '服务器繁忙，请稍后。'
            })

        # TODO: 用户状态保持 —— 把用户数据写入session，用于下一次请求验证用户身份。
        # 功能: 1. 用户信息写入session缓存; 2. 在响应中添加sessionid记录在cookie中
        login(request, user)
        # 4、构建响应
        response = JsonResponse({
            'code': 0,
            'errmsg': '恭喜，注册成功。'
        })

        # TODO: 在cookie中设置username记录登陆用户名作前端页面展示
        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)

        return response
