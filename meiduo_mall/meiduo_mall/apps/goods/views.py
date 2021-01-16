from django.shortcuts import render

# Create your views here.
# SearchView是haystack提供的一个视图类，对应的接口是：GET + /search/?q=华为
from haystack.views import SearchView
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage

from .models import SKU
from .utils import get_breadcrumb


# Create your views here.

class ListView(View):

    def get(self, request, category_id):
        # 1、提取参数
        page = request.GET.get('page')
        page_size = request.GET.get('page_size')
        ordering = request.GET.get('ordering')
        # 2、校验参数
        # 3、业务数据处理 —— 查询当前分类sku商品
        # 3.1、排序过滤出查询集
        skus = SKU.objects.filter(category_id=category_id).order_by(ordering)  # '-create_time'
        # 3.2、分页过滤出查询集
        # page=1&page_size=5
        # (1)、实例化分页器对象
        paginator = Paginator(skus, page_size)  # 根据每页page_size条数据，对skus查询集进行分页
        # (2)、获取指定页
        # page_skus是skus的一个子集，就是当前页查询集
        try:
            page_skus = paginator.page(page)  # 指定获取第page页
        except EmptyPage as e:
            return JsonResponse({'code': 400, 'errmsg': '指定页不存在'})

        # 3.3、把分页子集构建响应参数
        sku_list = []
        for sku in page_skus:
            sku_list.append({
                'id': sku.id,
                'default_image_url': sku.default_image.url,
                'name': sku.name,
                'price': sku.price
            })

        total_page = paginator.num_pages  # 总页数
        breadcrumb = get_breadcrumb(category_id)
        # 4、构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'breadcrumb': breadcrumb,
            'list': sku_list,
            'count': total_page
        })


# 搜索接口
class MySearchView(SearchView):

    # 改写默认搜索视图返回的响应数据
    def create_response(self):
        # 1、获取haystack从es中全文检索的结果
        context = self.get_context()  # 自动根据查询字符串参数q检索并且根据分页相关参数进行分页

        # 用户搜索词：context['query']
        # 分页器对象：context['paginator']
        # 默认每页数量：context['paginator'].per_page
        # 数据总量：context['paginator'].count

        # 当前页对象：context['page']
        # 搜索结果列表: context['page'].object_list
        # 搜索结果对象：SearchResult对象
        # 对应的模型类对象：SearchResult.object属性

        # 2、根据结果找到sku商品数据构建响应参数
        data_list = []
        for result in context['page'].object_list:
            # result: 是一个SearchResult对象
            sku = result.object
            data_list.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url,
                'searchkey': context['query'],
                'page_size': context['paginator'].num_pages,
                'count': context['paginator'].count
            })

        return JsonResponse(data_list, safe=False)


# 热销商品
class HotGoodsView(View):

    def get(self, request, category_id):
        # 1、提取参数
        # 2、校验参数
        # 3、业务数据处理 —— 根据销量降序排列返回2个
        skus = SKU.objects.filter(
            # category=GoodsCategory.objects.get(pk=category_id),
            category_id=category_id,  # 赋值为关联对象的主键值
            is_launched=True  # 只处理已经上架的商品
        ).order_by('-sales')  # 根据销量降序排列

        hot_sku_list = skus[0:2]  # QuerySet查询集支持下标切片操作
        hot_skus = []
        for sku in hot_sku_list:
            hot_skus.append({
                'id': sku.id,
                'default_image_url': sku.default_image.url,
                'name': sku.name,
                'price': sku.price
            })

        # 4、构建响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'hot_skus': hot_skus})
