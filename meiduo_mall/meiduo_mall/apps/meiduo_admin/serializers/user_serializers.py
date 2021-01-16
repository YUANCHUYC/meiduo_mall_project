from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'mobile',
            'email',

            'password',  # 补充password字段用作反序列化校验新建逻辑
        ]

        # 修改字段约束
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8, 'max_length': 20},  # password只参与反序列化
            'username': {'min_length': 3, 'max_length': 20},
        }

    # 校验的过程中介入来密码加密和is_staff设置为True
    # def validate(self, attrs):
    #     attrs['is_staff'] = True
    #     raw_password = attrs.get('password') # 明文密码
    #     attrs['password'] = make_password(raw_password)# 密文密码
    #     return attrs

    # 新建保存的过程中介入来密码加密和is_staff设置为True
    def create(self, validated_data):
        # validated_data有效数据中追加is_staff=True
        validated_data['is_staff'] = True
        # 新建用户需要加密密码
        instance = User.objects.create_user(**validated_data)
        return instance
