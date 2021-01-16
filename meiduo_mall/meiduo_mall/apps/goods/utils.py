from .models import GoodsCategory


def get_breadcrumb(category_id):
    """
    获取导航数据
    :param category_id: 分类id
    :return: 字典
    """
    # 根据传入的分类的id，构建1，2，3级分类导航
    category = GoodsCategory.objects.get(pk=category_id)
    # (1)、如果传来的是一级分类
    if not category.parent:
        return {
            'cat1': category.name
        }
    # (2)、如果传来的是二级分类
    if not category.parent.parent:
        return {
            'cat1': category.parent.name,
            'cat2': category.name
        }
    # (3)、如果传来的是三级分类
    if not category.parent.parent.parent:
        return {
            'cat1': category.parent.parent.name,
            'cat2': category.parent.name,
            'cat3': category.name
        }
