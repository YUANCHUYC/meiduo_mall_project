"""
管理员用户管理
"""

from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from users.models import User


# 新建用户可选分组
class AdminGroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
            'name'
        ]


class AdminModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'mobile',

            'password',

            'groups',  # 新建用户从属分组
            'user_permissions'  # 新建用户拥有的权限
        ]

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        # 密码加密，is_staff=True
        attrs['is_staff'] = True
        raw_password = attrs.get('password')  # 明文
        attrs['password'] = make_password(raw_password)  # 密文
        return attrs
