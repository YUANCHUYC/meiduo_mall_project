#! /usr/bin/env python3

"""
python编写的脚本文件
功能：执行该脚本，批量生成所有sku商品的静态化页面
"""
import os,sys
import django

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# TODO：加载django环境
# (1)、设置配置文件导包路径
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings.dev')
# (2)、手动加载
django.setup()

from django.conf import settings
from django.template import loader
from contents.utils import get_categories
from goods.utils import get_breadcrumb,get_goods_and_spec
from goods.models import SKU

# 生成sku商品静态化页面
# 参数：sku是传入的SKU模型类对象
def generate_static_sku_detail_html(sku):
    categories = get_categories()
    breadcrumb = get_breadcrumb(sku.category.id)
    goods, sku, specs = get_goods_and_spec(sku.id)

    # 1、构建模版参数
    context = {
        'categories': categories,  # 渲染分类
        'breadcrumb': breadcrumb,  # 渲染导航
        'goods': goods,  # 商品价格等信息
        'sku': sku,  # 商品价格等信息
        'specs': specs,  # 商品规格信息
    }

    # 2、获取模版对象
    template = loader.get_template('detail.html')
    # 3、渲染页面
    html = template.render(context=context)

    detail_html_dir = os.path.join(
        os.path.dirname(os.path.dirname(settings.BASE_DIR)),
        'front_end_pc/goods'
    )

    # 4、保存静态文件 —— front_end_pc/goods文件夹中保存，并且以sku的id作为文件名
    with open(os.path.join(detail_html_dir, '%d.html'%sku.id), 'w') as f:
        f.write(html)


if __name__ == '__main__':
    skus = SKU.objects.filter(is_launched=True)
    for sku in skus:
        generate_static_sku_detail_html(sku)