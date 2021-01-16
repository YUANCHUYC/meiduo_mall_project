from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

import os

from alipay import AliPay

from django.conf import settings
from orders.models import OrderInfo
from .models import Payment


# Create your views here.


class PaymentView(View):

    def get(self, request, order_id):
        # 1、提取参数
        # 2、校验参数
        # 3、业务数据处理 —— 调用支付宝sdk来构建扫码页面链接参数
        # (1)、实例化AliPay对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 支付成功之后阿里服务器主动请求的美多商城链接(线上服务器)
            app_private_key_path=os.path.join(
                os.path.dirname(os.path.abspath(__file__)),  # payment文件夹的绝对路径
                'keys/app_private_key.pem'
            ),
            alipay_public_key_path=os.path.join(
                os.path.dirname(os.path.abspath(__file__)),  # payment文件夹的绝对路径
                'keys/alipay_public_key.pem'
            ),
            debug=settings.ALIPAY_DEBUG
            # sign_type='RSA2', # 加密算法
        )

        order = OrderInfo.objects.get(pk=order_id)

        # (2)、找对象的方法来构建支付链接参数
        # 支付完整的链接 = 'https://openapi.alipaydev.com/gateway.do' + '?' +  支付链接参数(查询字符串参数)
        order_string = alipay.api_alipay_trade_page_pay(
            '美多商城订单：%s' % order_id,
            out_trade_no=order_id,  # 客户(美多商城)订单号
            total_amount=float(order.total_amount),  # Decimal转化为普通的float
            return_url=settings.ALIPAY_RETURN_URL
        )

        alipay_url = settings.ALIPAY_URL + '?' + order_string
        # 4、构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'alipay_url': alipay_url
        })


# 支付成功保存支付订单
class PaymentStatusView(View):

    def put(self, request):
        # 1、提取参数
        # 查询字符串参数在django中提取的出QueryDict类型。支付宝后续的接口要求传入普通字典，所以此处我们转化为字典
        # data = dict(request.GET) # 错误代码，如果强转QueryDict那么value是一个列表类型，显然是错误的
        data = request.GET.dict()  # 使用QueryDict.dict()函数转化字典的时候，只保留一个value
        sign = data.pop('sign')  # 把sign签名数据提取出来，并从原字典中删除

        # 2、校验参数
        # (1)、获取alipay对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 支付成功之后阿里服务器主动请求的美多商城链接(线上服务器)
            app_private_key_path=os.path.join(
                os.path.dirname(os.path.abspath(__file__)),  # payment文件夹的绝对路径
                'keys/app_private_key.pem'
            ),
            alipay_public_key_path=os.path.join(
                os.path.dirname(os.path.abspath(__file__)),  # payment文件夹的绝对路径
                'keys/alipay_public_key.pem'
            ),
            debug=settings.ALIPAY_DEBUG
            # sign_type='RSA2', # 加密算法
        )
        # (2)、校验支付数据
        if not alipay.verify(data, sign):
            return JsonResponse({'code': 400, 'errmsg': '支付数据验证失败'})

        # 3、业务数据处理 —— 保存支付订单

        # 3.1、提取订单信息
        order_id = data.get('out_trade_no')  # 美多商城订单号
        trade_id = data.get('trade_no')  # 支付宝订单号

        # 3.2、新建支付订单
        Payment.objects.create(
            order_id=order_id,
            trade_id=trade_id
        )

        # 3.3、修改美多商城订单状态
        order = OrderInfo.objects.get(pk=order_id)
        order.status = OrderInfo.ORDER_STATUS_ENUM['UNSEND']
        order.save()

        # 4、构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'trade_id': trade_id
        })
