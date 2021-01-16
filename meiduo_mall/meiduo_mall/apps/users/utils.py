"""
继承ModelBackend，自定义认证后端
"""

from django.contrib.auth.backends import ModelBackend
from .models import User
from django.db.models import Q
from meiduo_mall.utils.secret import SecretOauth
from django.conf import settings


class UsernameMobileAuthBackend(ModelBackend):

    # 重写该方法，实现根据username过滤，或根据mobile过滤用户对象
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 查找用户
        try:
            user = User.objects.get(
                Q(username=username) | Q(mobile=username)
            )
        except User.DoesNotExist as e:
            # 如果抛出异常，说明账号有误，认证失败，返回None
            return None

        # 校验密码
        if not user.check_password(password):
            return None

        # 认证成功返回用户对象
        return user


# 构造验证链接verify_url
def generate_verify_email_url(request):
    """
    功能: 加密用户数据成token，拼接完成的验证链接verify_url返回
    参数：request请求对象 —— 通过请求对象获取user用户对象
    返回值：完整的验证链接
    """
    # 加密获取token值
    token = SecretOauth().dumps({
        'user_id': request.user.id,
        'username': request.user.username,
        'email': request.user.email
    })
    # 拼接完整验证链接
    verify_url = settings.EMAIL_VERIFY_URL + token

    return verify_url
