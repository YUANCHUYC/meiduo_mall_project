"""
权限表管理序列化器
"""
from django.contrib.auth.models import Permission, ContentType
from rest_framework import serializers


# 新建权限可选类型
class ContentTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = [
            'id',
            'name'
        ]


class PermModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'id',
            'name',
            'codename',
            'content_type'
        ]
