"""
spu管理序列化器
"""
from rest_framework import serializers
from goods.models import SPU, Brand, GoodsCategory


# SPU序列化器
class SPUModelSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField()

    category1_id = serializers.IntegerField()
    category2_id = serializers.IntegerField()
    category3_id = serializers.IntegerField()

    class Meta:
        model = SPU
        exclude = ['category1', 'category2', 'category3']


# Brand品牌表序列化器
class BrandSimpleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'id',
            'name'
        ]


# 新建SPU可选分类序列化器
class CateSimpleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = [
            'id',
            'name'
        ]
