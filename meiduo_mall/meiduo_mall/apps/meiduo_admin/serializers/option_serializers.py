"""
定义选项表管理的序列化器
"""
from rest_framework import serializers
from goods.models import SpecificationOption, SPUSpecification


# 新建选项可选规格
class SpecSimpleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPUSpecification
        fields = [
            'id',
            'name'
        ]


class OptionModelSerializer(serializers.ModelSerializer):
    spec = serializers.StringRelatedField()
    spec_id = serializers.IntegerField()

    class Meta:
        model = SpecificationOption
        fields = [
            'id',
            'value',
            'spec',
            'spec_id'
        ]
