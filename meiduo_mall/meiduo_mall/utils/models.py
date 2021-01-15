from django.db import models


# 模型类抽象基类：只是用于被继承补充字段的，不应该生成表。
class BaseModel(models.Model):
    """为模型类补充字段"""

    # 创建时间:           年月日时分秒    新建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 更新时间:           年月日时分秒    自动设置为数据更新的时间
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # 说明是抽象模型类(抽象模型类不会创建表)
        abstract = True
