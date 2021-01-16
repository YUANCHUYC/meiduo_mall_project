from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django_redis import get_redis_connection
from .libs.captcha.captcha import captcha
# from .libs.yuntongxun.ccp_sms import CCP
from celery_tasks.sms.tasks import ccp_send_sms_code
import re, random


# Create your views here.

class ImageCodeView(View):

    def get(self, request, uuid):
        # 1、提取参数
        # 2、校验参数
        # 3、业务数据处理——使用captcha生成图片验证码，写入redis、响应图片数据
        # 3.1、调用captcha生成图片和验证码
        text, image = captcha.generate_captcha()
        print("验证码:", text)
        # 3.2、把验证码写入redis
        # 约定格式：{ img_<uuid> : text }
        # get_redis_connection: 根据django的配置获取一个redis的链接对象
        conn = get_redis_connection('verify_code')
        conn.setex('img_%s' % uuid, 300, text)
        # 4、构建响应
        return HttpResponse(
            image,  # 图片数据，作为响应体数据
            content_type='image/jpeg'
        )


# 短信验证码接口
class SMSCodeView(View):

    def get(self, request, mobile):
        # 1、提取参数
        image_code = request.GET.get('image_code')
        image_code_id = request.GET.get('image_code_id')
        # 2、校验参数
        # 2.1、必要校验
        if not all([image_code, image_code_id]):
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'}, status=400)
        # 2.2、约束校验
        if not re.match(r'^[a-zA-Z0-9]{4}$', image_code):
            return JsonResponse({'code': 400, 'errmsg': '图形验证码格式有误'}, status=400)
        if not re.match(r'^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$', image_code_id):
            return JsonResponse({'code': 400, 'errmsg': 'uuid有误！'}, status=400)
        # 2.3、业务校验 —— 校验用户填写的图形验证码image_code和redis存储的是否一致
        # TODO: 对比图形验证码
        conn = get_redis_connection('verify_code')  # 2号库
        # (1)、根据前端传来的uuid(image_code_id)读取redis中图形验证码
        image_code_from_redis = conn.get('img_%s' % image_code_id)  # 如果过期返回None，存在返回b"LTBG"
        # TODO: 为了防止验证码被重复校验，我们只允许被校验一次  —— 凡是读一次redis验证码，就直接删除
        conn.delete('img_%s' % image_code_id)
        if not image_code_from_redis:
            # 过期了
            return JsonResponse({'code': 400, 'errmsg': '图形验证码失效'}, status=400)
        # (2)、和用户输入的验证码比对 —— 忽略大小写
        if image_code.lower() != image_code_from_redis.decode().lower():
            return JsonResponse({'code': 400, 'errmsg': '验证码输入有误'}, status=400)

        # 3、业务数据处理 —— 发短信，redis存短信验证码
        # TODO: 先判断短信发送标志信息是否存在
        flag = conn.get('send_flag_%s' % mobile)  # b'-1' or None
        if flag:
            return JsonResponse({'code': 400, 'errmsg': '请勿重复发送'}, status=400)

        sms_code = "%06d" % random.randrange(0, 999999)
        print("手机验证码: ", sms_code)
        # TODO: 使用yuntongxun发短信
        # (1)、初始化CCP对象
        # ccp = CCP()
        # (2)、发送短信
        # ccp.send_template_sms(
        #     mobile,
        #     [sms_code, 5],
        #     1
        # )
        # TODO: 以异步的方式发送短信 —— 发布任务
        ccp_send_sms_code.delay(mobile, sms_code)

        # TODO: 把短信验证码存入redis --> sms_手机号 ：sms_code
        # conn.setex('sms_%s'%mobile, 300, sms_code)
        # TODO: 添加标志信息，记录60秒内发送过短信
        # conn.setex('send_flag_%s'%mobile, 60, -1)
        # TODO: 优化，使用redis的pipeline功能，把多条redis命令批量执行
        # (1)、获取pipeline对象
        p = conn.pipeline()
        # (2)、调用pipeline对象的方法，把指令加入执行队列中 —— 只是加入队列，未执行
        p.setex('sms_%s' % mobile, 300, sms_code)
        p.setex('send_flag_%s' % mobile, 60, -1)
        # (3)、批量执行 —— 真正发生网络通信
        p.execute()

        # 4、构建响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
