from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from django.core.cache import cache

from .models import Area


# Create your views here.

# 获取省级行政区信息
class ProvinceAreasView(View):

    def get(self, request):
        # 1、提取数据
        # 2、校验数据
        # 3、业务数据处理 —— 过滤出省信息构建响应参数
        # TODO: 读缓存
        province_list = cache.get('province_list')  # 读到的数据 or None

        if not province_list:
            # 没有读到缓存数据，才需要到mysql中读取
            try:
                provinces = Area.objects.filter(
                    parent=None
                )
            except Exception as e:
                return JsonResponse({'code': 400, 'errmsg': '服务器内部错误'})

            province_list = []
            for province in provinces:
                # province是Area对象(省)
                province_list.append({
                    'id': province.id,
                    'name': province.name
                })

            # TODO: 写入缓存
            cache.set('province_list', province_list, 3600)

        # 4、构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'province_list': province_list
        })


# 获取子级行政区信息
class SubAreasView(View):

    def get(self, request, pk):
        # 初始化一个变量记录后续需要返回给前端的数据
        sub_data = cache.get('sub_area_%s' % pk)  # 读取到数据 or None

        # 1、提取参数
        # 2、校验参数
        # 3、业务数据处理 —— 过滤出子级行政区信息
        if not sub_data:
            # 当且仅当缓存无数据，才需要从mysql读
            try:
                parent = Area.objects.get(pk=pk)
                subs = parent.subs.all()
            except Exception as e:
                return JsonResponse({'code': 400, 'errmsg': '数据库内部错误'})

            subs_list = []
            for sub in subs:
                # sub是子级行政区对象
                subs_list.append({
                    'id': sub.id,
                    'name': sub.name
                })

            # 构建响应参数
            sub_data = {
                'id': parent.id,
                'name': parent.name,
                'subs': subs_list
            }

            # TODO: 写缓存 --> {"sub_area_340000": [{......}]}
            cache.set('sub_area_%s' % parent.id, sub_data, 3600)

        # 4、构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'sub_data': sub_data
        })
