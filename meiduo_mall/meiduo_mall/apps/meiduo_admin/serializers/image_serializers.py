"""
图片管理序列化器
"""
from rest_framework import serializers
from goods.models import SKUImage, SKU


class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKUImage
        fields = [
            'id',
            'sku',  # sku是关联主表对象，默认映射的类型是PrimaryKeyRelatedFiel序列化结果就是sku的id值
            'image'  # image是ImageField类型字段，序列化的结果是存储后端url()函数返回的结果
        ]


# 新建图片可选sku
class SKUSimpleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = [
            'id',
            'name'

        ]
