from django.db import models


# Create your models here.
class Area(models.Model):
    """
    行政区划
    """
    # 创建 name 字段, 用户保存名称
    name = models.CharField(max_length=20, verbose_name='名称')
    # 自关联字段 parent
    # related_name='subs' --> ForeignKey外间字段通过related_name约束条件，设置主表隐藏字段subs
    # 主表隐藏字段subs记录的是当前主表对象关联的多个从表对象，是一个查询集。
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True,
                               verbose_name='上级行政区划')

    class Meta:
        db_table = 'tb_areas'

    def __str__(self):
        return self.name
