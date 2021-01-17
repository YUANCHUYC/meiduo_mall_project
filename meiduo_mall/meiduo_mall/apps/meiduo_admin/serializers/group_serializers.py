"""
分组管理序列化器
"""

from django.contrib.auth.models import Group, Permission
from rest_framework import serializers


# 新建分组可选权限
class PermSimpleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'id',
            'name'
        ]


class GroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
            'name',

            'permissions'
        ]

    # def create(self, validated_data):
    #     # 经过有效校验之后，permissions中记录的就是权限对象;permissions = [<吃饭:102>, <睡觉:103>, <打豆豆:104>]
    #     # (1)、把权限从有效数据中提出
    #     permissions = validated_data.pop('permissions')
    #     # (2)、新建分组
    #     group = Group.objects.create(**validated_data)
    #     # (3)、插入分组权限中间表
    #     group.permissions.set(permissions)
    #     return group
