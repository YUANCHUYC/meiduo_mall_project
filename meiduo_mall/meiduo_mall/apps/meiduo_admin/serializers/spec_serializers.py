"""
定义规格表管理序列化器
"""

from rest_framework import serializers
from goods.models import SPUSpecification


class SpecModelSerializer(serializers.ModelSerializer):
    spu = serializers.StringRelatedField()
    spu_id = serializers.IntegerField()

    class Meta:
        model = SPUSpecification
        fields = [
            'id',
            'name',
            'spu',  # 序列化规格(从),嵌套序列化关联SPU(主)单一对象。
            'spu_id'
        ]
