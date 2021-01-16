"""
定义关于SKU管理中的序列化器
"""
from django.db import transaction
from rest_framework import serializers
from goods.models import SKU, SKUSpecification, GoodsCategory, SPU, SPUSpecification, SpecificationOption


class SKUSpecOptModelSerializer(serializers.ModelSerializer):
    spec_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

    class Meta:
        model = SKUSpecification
        fields = [
            'spec_id',
            'option_id'
        ]


# SKU序列化器
class SKUModelSerializer(serializers.ModelSerializer):
    spu = serializers.StringRelatedField()
    # spu_id是关联主表单一对象的主键隐藏字段
    spu_id = serializers.IntegerField()
    category = serializers.StringRelatedField()
    # category_id是关联主表单一对象的主键隐藏字段
    category_id = serializers.IntegerField()

    # 关联从表隐藏字段
    # 记录关联的多个SKUSpecfication模型类对象数据
    # 总结：序列化主表SKU数据的时候，嵌套序列化与之关联的多个从表SKUSpecificatoin对象数据
    specs = SKUSpecOptModelSerializer(many=True)

    class Meta:
        model = SKU
        # 模型类显示定义的字段 和 主键隐藏字段 自动映射
        fields = "__all__"

    # specs字段记录的是sku的规格和选项信息
    # 注意：该字段是用来新建中间表SKUSpecification数据的,而模型类序列化器默认create方法
    # 无法完成中间表数据的新建,所以我们需要重写
    def create(self, validated_data):
        # 1、提取规格和选项信息
        # specs = [{"spec_id": 4, "option_id": 8}, ...]
        specs = validated_data.pop('specs')  # 这里把specs重有效数据中pop出，后续新建sku用不着specs
        with transaction.atomic():
            save_point = transaction.savepoint()

            try:
                # 2、新建主表SKU数据
                sku = SKU.objects.create(**validated_data)
                # 3、根据specs新建中间表数据SKUSpecification以此来记录新建的sku拥有的规格和选项信息
                for spec in specs:
                    # spec = {"spec_id": 4, "option_id": 8}
                    spec['sku_id'] = sku.id  # {"sku_id": 17, spec_id": 4, "option_id": 8}
                    SKUSpecification.objects.create(**spec)
            except Exception as e:
                transaction.rollback(save_point)

            transaction.savepoint_commit(save_point)

        return sku

    # specs字段记录的是sku的新的规格和选项信息
    # 注意：该字段是用来更新中间表SKUSpecification数据的,而模型类序列化器默认update方法
    # 无法完成中间表数据的更新,所以我们需要重写
    def update(self, instance, validated_data):
        # 1、提取新的规格和选项信息
        # specs = [{"spec_id": 6, "option_id": 13}, ....]
        specs = validated_data.pop('specs')

        with transaction.atomic():
            save_point = transaction.savepoint()

            try:
                # 2、更新主表SKU数据
                sku = super().update(instance, validated_data)
                # 3、根据新的规格和选项去更新中间表
                # (1)、先删除原有中间表数据
                SKUSpecification.objects.filter(sku_id=sku.id).delete()
                # (2)、在插入新的规格和选项
                for spec in specs:
                    # spec = {"spec_id": 6, "option_id": 13}
                    spec['sku_id'] = sku.id  # {"spec_id": 6, "option_id": 13, "sku_id": 17}
                    SKUSpecification.objects.create(**spec)
            except Exception as e:
                transaction.savepoint_rollback(save_point)

            transaction.savepoint_commit(save_point)

        return sku


# 分类序列化器
class SKUGoodsCateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = [
            'id',
            'name'
        ]


# SPU序列化器
class SPUSimpleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPU
        fields = [
            'id',
            'name'
        ]


# 选项SpecificationOption序列化器
class OptSimpleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationOption
        fields = [
            'id',
            'value'
        ]


# 规格SPUSpecification序列化器
class SpecSimpleModelSerializer(serializers.ModelSerializer):
    spu = serializers.StringRelatedField()
    spu_id = serializers.IntegerField()

    # 关联从表选项表SpecificationOption多个对象
    # 总结：序列化主表规格表SPUSpecification对象的时候，嵌套序列化与之关联的多个从表选项表SpecificationOption对象
    options = OptSimpleModelSerializer(many=True)

    class Meta:
        model = SPUSpecification
        fields = [
            'id',
            'name',
            'spu',
            'spu_id',
            'options'
        ]
