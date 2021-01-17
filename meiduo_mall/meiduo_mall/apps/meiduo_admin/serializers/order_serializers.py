'''
定义订单序列化器
'''
from rest_framework import serializers
from orders.models import OrderInfo, OrderGoods
from goods.models import SKU


# 订单简单序列化器用于 列表数据返回
class OrderSimpleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = [
            'order_id',
            'create_time',
            'status'
        ]

        extra_kwargs = {
            'create_time': {'format': '%Y/%m/%d'},
            'status': {'write_only': True}
        }


# 自定义SKU序列化器
class SKUSimpleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = [
            'name',
            'default_image'
        ]


# 定义OrderGoods序列化器
class OrderGoodsModelSerializer(serializers.ModelSerializer):
    # sku是关联的SKU主表单一对象
    sku = SKUSimpleModelSerializer()

    class Meta:
        model = OrderGoods
        fields = [
            'count',
            'price',
            'sku'
        ]


# 订单详情序列化器用于 单一订单详情序列化返回
class OrderDetailModelSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    # skus是关联的从表OrderGoods多条对象数据
    skus = OrderGoodsModelSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"
