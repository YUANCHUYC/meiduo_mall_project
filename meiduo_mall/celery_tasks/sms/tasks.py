"""
在一个任务包sms里面定义一个固定名称的模块tasks.py，在tasks.py模块中定义任务函数
"""
from celery_tasks.main import celery_app
from celery_tasks.yuntongxun.ccp_sms import CCP

# 定义一个发送短信的异步任务函数
@celery_app.task(name='ccp_send_sms_code')
def ccp_send_sms_code(mobile, sms_code):
    """
    功能：使用yuntongxun发送短信
    参数：mobile手机号，sms_code验证码
    :return: 云通讯发送短信接口的返回值返回
    """
    ccp = CCP()
    result = ccp.send_template_sms(
        mobile,
        [sms_code, 5],
        1
    )
    return result