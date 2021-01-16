"""
1、在被搜索数据模型类SKU所在应用goods中，新建一个固定名称的模块search_indexes.py
2、在search_indexes.py中定义一个索引模型类SKUIndex，索引模型类名称格式：<被搜索的模型类名>Index
3、定义模版文件
"""

from haystack import indexes
from .models import SKU


class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """SKU索引数据模型类"""
    # 约定俗称的字段text，类型为indexes.CharField。
    # document=True表明：该字段，决定了，我们可以根据SKU模型类的哪些属性进行全文检索。
    # use_template=True表明：通过模版文件的方式来指定SKU模型类属性。
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return SKU

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter(is_launched=True)  # 返回所有上架的SKU查询集
