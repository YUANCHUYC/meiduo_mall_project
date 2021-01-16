from django.core.mail import send_mail
from django.conf import settings
from celery_tasks.main import celery_app


# 封装一个任务函数 —— 发邮件
@celery_app.task(name='send_verify_email')
def send_verify_email(to_email, verify_url):
    """
    功能：发验证邮件
    :param to_email: 收件人 —— 用于保存更新的邮箱
    :param verify_url: 验证邮件中的 链接
    :return: 1成功，0失败
    """

    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)

    result = send_mail(
        '美多商城',
        '',
        from_email=settings.EMAIL_FROM,
        recipient_list=[to_email],
        html_message=html_message
    )
    return result
