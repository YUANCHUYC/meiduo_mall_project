from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django_redis import get_redis_connection

import json

from goods.models import SKU
from meiduo_mall.utils.cookiesecret import CookieSecret


# Create your views here.

class CartsView(View):

    # 添加购物车
    def post(self, request):
        # 1、提取参数
        data = json.loads(request.body.decode())
        sku_id = data.get('sku_id')
        count = data.get('count')
        selected = data.get('selected', True)  # 默认勾选

        # 2、校验参数
        if not all([sku_id, count]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必要字段'})

        try:
            sku = SKU.objects.get(pk=sku_id)
        except SKU.DoesNotExist as e:
            return JsonResponse({'code': 400, 'errmsg': 'sku不存在'})

        # 3、业务数据处理
        user = request.user
        if user.is_authenticated:
            # 3.1、登陆 —— 存入redis
            conn = get_redis_connection('carts')  # 5号
            # (1)、存哈希对象 —— 商品和数量
            # 如果当前sku_id在哈希对象里面，需要把count累加
            # conn.hmset('carts_%s'%user.id, {sku_id:count})
            conn.hincrby('carts_%s' % user.id, sku_id, count)  # 如果sku_id存在则累加，不存在则新增
            # (2)、存集合 —— 记录选中状态
            if selected:
                conn.sadd('selected_%s' % user.id, sku_id)
            else:
                conn.srem('selected_%s' % user.id, sku_id)
            return JsonResponse({'code': 0, 'errmsg': 'ok'})
        else:
            # 3.2、未登陆 —— 存入cookie
            # (1)、当前请求cookie里面是否已经有购物车数据了
            cookie_str = request.COOKIES.get('carts')  # carts是存入cookie的购物车数据的key
            if cookie_str:
                # cookie有购物车数据，需要解密得到购物车字典数据
                cart_dict = CookieSecret.loads(cookie_str)
            else:
                # cookie中没有购物车数据
                cart_dict = {}

            # (2)、追加当前新增的商品
            if sku_id in cart_dict:
                # 把数量累加
                cart_dict[sku_id]['count'] += count
                cart_dict[sku_id]['selected'] = selected
            else:
                cart_dict[sku_id] = {
                    'count': count,
                    'selected': selected
                }

            # (3)、把最新的cookie购物车字典数据，编码成字符串写入cookie
            cookie_str = CookieSecret.dumps(cart_dict)
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            response.set_cookie('carts', cookie_str, max_age=14 * 3600 * 24)
            return response

    # 查询购物车，展示购物车
    def get(self, request):
        # 后续为了方便业务数据组织，从redis或者cookie读取的购物车数据，统一组成字典数据
        cart_dict = {}  # 购物车字典数据，{1: {"count": 5, "selected": True}}

        user = request.user
        if user.is_authenticated:
            # 登陆
            conn = get_redis_connection('carts')
            # (1)、读取购物车商品数量，哈希数据
            # redis_carts = {b'1': b'5', b'2': b'3'}
            redis_carts = conn.hgetall('carts_%s' % user.id)
            # (2)、购物车选中状态，集合数据
            # redis_selected = [b'1', b'2']
            redis_selected = conn.smembers('selected_%s' % user.id)
            # (3)、把redis购物车数据，转化成购物车字典数据
            sku_ids = redis_carts.keys()
            for sku_id in sku_ids:
                # sku_id = b'1'
                cart_dict[int(sku_id)] = {
                    'count': int(redis_carts[sku_id]),
                    'selected': sku_id in redis_selected
                }
        else:
            # 未登陆
            cookie_str = request.COOKIES.get('carts')
            if cookie_str:
                cart_dict = CookieSecret.loads(cookie_str)
            else:
                cart_dict = {}

        # 读取mysql获取sku商品的详细信息，组织响应参数
        sku_ids = cart_dict.keys()  # [1,2]
        cart_skus = []
        for sku_id in sku_ids:
            sku = SKU.objects.get(pk=sku_id)
            cart_skus.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price,
                'count': cart_dict[sku_id]['count'],
                'selected': cart_dict[sku_id]['selected']
            })

        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'cart_skus': cart_skus
        })

    # 更新购物车
    def put(self, request):
        # 1、提取参数
        data = json.loads(request.body.decode())
        sku_id = data.get('sku_id')
        count = data.get('count')
        selected = data.get('selected', True)

        # 2、校验参数
        if not all([sku_id, count]):
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'})

        try:
            sku = SKU.objects.get(pk=sku_id)
        except SKU.DoesNotExist as e:
            return JsonResponse({'code': 400, 'errmsg': '商品不存在'})

        # 3、业务数据处理
        user = request.user
        if user.is_authenticated:
            # 登陆，修改redis购物车
            conn = get_redis_connection('carts')
            # (1)、修改商品数量 —— 哈希对象设置键值对默认覆盖原值
            conn.hset('carts_%s' % user.id, sku_id, count)
            # (2)、修改选中状态
            if selected:
                conn.sadd('selected_%s' % user.id, sku_id)
            else:
                conn.srem('selected_%s' % user.id, sku_id)
            return JsonResponse({'code': 0, 'errmsg': 'ok'})
        else:
            # 未登陆，修改cookie购物车
            # (1)、读取cookie购物车字典数据
            cookie_str = request.COOKIES.get('carts')
            if cookie_str:
                cart_dict = CookieSecret.loads(cookie_str)
            else:
                cart_dict = {}
            # (2)、修改为新数据
            if sku_id in cart_dict:
                cart_dict[sku_id]['count'] = count
                cart_dict[sku_id]['selected'] = selected
            # (3)、重新加密写入cookie
            cookie_str = CookieSecret.dumps(cart_dict)
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            response.set_cookie('carts', cookie_str)
            return response

    # 删除购物车
    def delete(self, request):
        # 1、提取参数
        data = json.loads(request.body.decode())
        sku_id = data.get('sku_id')
        # 2、校验参数
        if not sku_id:
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'})
        try:
            sku = SKU.objects.get(pk=sku_id)
        except SKU.DoesNotExist as e:
            return JsonResponse({'code': 400, 'errmsg': '商品不存在'})

        # 3、业务数据处理
        user = request.user
        if user.is_authenticated:
            # 登陆，删除redis购物车指定sku商品数据
            conn = get_redis_connection('carts')
            # (1)、把sku_id从哈希对象中删除
            conn.hdel('carts_%s' % user.id, sku_id)
            # (2)、把sku_id从集合中删除
            conn.srem('selected_%s' % user.id, sku_id)
            response = JsonResponse({
                'code': 0, 'errmsg': 'ok'
            })
            return response

        else:
            # 未登陆，删除cookie购物车指定sku商品数据
            # (1)、读取cookie购物车字典数据
            cookie_str = request.COOKIES.get('carts')
            if cookie_str:
                cart_dict = CookieSecret.loads(cookie_str)
            else:
                cart_dict = {}
            # (2)、删除指定sku_id
            if sku_id in cart_dict:
                # del cart_dict[sku_id] 删除字典的键值对
                cart_dict.pop(sku_id)
            # (3)、重新加密设置在cookie中
            cookie_str = CookieSecret.dumps(cart_dict)
            response = JsonResponse({
                'code': 0, 'errmsg': 'ok'
            })
            response.set_cookie('carts', cookie_str)
            return response


# 全选购物车
class CartsSelectAllView(View):

    def put(self, request):
        data = json.loads(request.body.decode())
        selected = data.get('selected')  # 没有传就是None

        # 判读selected类型，必须是bool类型(True or False)
        if not isinstance(selected, bool):
            return JsonResponse({'code': 400, 'errmsg': '参数有误'})

        # 业务数据处理
        user = request.user
        if user.is_authenticated:
            # 登陆，把redis购物车全部商品选中
            conn = get_redis_connection('carts')
            # (1)、获取所有sku商品
            # redis_carts = {b'1':b'5', b'2': b'6'}
            redis_carts = conn.hgetall('carts_%s' % user.id)
            # (2)、把所有sku商品的id加入集合
            sku_ids = redis_carts.keys()  # [b'1', b'2']
            if selected:
                conn.sadd('selected_%s' % user.id, *sku_ids)  # *sku_ids对列表进行拆包：(*sku_ids) = (b'1', b'2')
            else:
                conn.srem('selected_%s' % user.id, *sku_ids)
            return JsonResponse({'code': 0, 'errmsg': 'ok'})
        else:
            # 未登陆，把cookie购物车中的全部商品选中
            # (1)、读取cookie购物车字典
            cookie_str = request.COOKIES.get('carts')
            if cookie_str:
                cart_dict = CookieSecret.loads(cookie_str)
            else:
                cart_dict = {}
            # (2)、把购物车字典中所有对商品的selected设置未True
            sku_ids = cart_dict.keys()
            for sku_id in sku_ids:
                cart_dict[sku_id]['selected'] = selected  # 前端传来的selected是True表示全选，为False表示全部取消
            # (3)、加密新字典写入cookie
            cookie_str = CookieSecret.dumps(cart_dict)
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            response.set_cookie('carts', cookie_str)
            return response


# 简单购物车展示
class CartsSimpleView(View):

    def get(self, request):
        user = request.user

        # 初始化一个空的购物车字典数据，用于记录后续redis或者cookie中读取的购物车
        cart_dict = {}  # {1: {"count": 5, "selected": True}}

        if user.is_authenticated:
            # (1)、登陆读取redis
            conn = get_redis_connection('carts')
            # redis_carts = {b'1': b'5'}
            redis_carts = conn.hgetall('carts_%s' % user.id)
            # redis_selected = [b'1']
            redis_selected = conn.smembers('selected_%s' % user.id)

            # 构建统一约定好的购物车字典数据 —— 只处理选中
            sku_ids = redis_carts.keys()  # [b'1']
            for sku_id in sku_ids:
                if sku_id in redis_selected:  # b'1' in [b'1']
                    cart_dict[int(sku_id)] = {
                        'count': int(redis_carts[sku_id]),
                        'selected': sku_id in redis_selected  # True
                    }

        else:
            # (2)、未登陆读取cookie
            cookie_str = request.COOKIES.get('carts')
            if cookie_str:
                cart_dict = CookieSecret.loads(cookie_str)
            else:
                cart_dict = {}

            # 我们把keys返回的迭代器强转为列表，后续遍历的是列表中保存的所有选中的sku_id。
            # 这样我们就可以改变购物车字典的长度 —— 删除key
            sku_ids = list(cart_dict.keys())  # [1,2]
            for sku_id in sku_ids:
                if not cart_dict[sku_id]['selected']:  # 表示当前sku商品在cookie购物车字典中未选项
                    cart_dict.pop(sku_id)

        # (3)、构建响应参数 —— 读mysql
        sku_ids = cart_dict.keys()  # 一定都是选择的商品
        cart_skus = []
        for sku_id in sku_ids:
            sku = SKU.objects.get(pk=sku_id)
            cart_skus.append({
                'id': sku.id,
                'name': sku.name,
                'count': cart_dict[sku_id]['count'],
                'default_image_url': sku.default_image.url
            })

        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'cart_skus': cart_skus
        })
