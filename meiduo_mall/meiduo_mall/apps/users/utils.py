"""
继承ModelBackend，自定义认证后端
"""

from django.contrib.auth.backends import ModelBackend
from .models import User
from django.db.models import Q


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
