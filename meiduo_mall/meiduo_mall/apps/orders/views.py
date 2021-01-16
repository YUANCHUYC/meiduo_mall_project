from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.utils import timezone
from django_redis import get_redis_connection
from django.db import transaction

from decimal import Decimal
import json

from users.models import Address, User
from goods.models import SKU
from orders.models import OrderGoods, OrderInfo

from meiduo_mall.utils.views import LoginRequiredJSONMixin


# Create your views here.


# 订单结算
class OrderSettlementView(LoginRequiredJSONMixin, View):

    def get(self, request):
        # 1、提取参数
        user = request.user
        # 2、校验参数
        # 3、业务数据处理
        # 3.1、获取当前登陆用户管理的收货地址
        addresses = user.addresses.filter(is_deleted=False)
        # 构建字典响应数据
        address_list = []
        for address in addresses:
            address_list.append({
                'id': address.id,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'place': address.place,
                'mobile': address.mobile,
                'receiver': address.receiver
            })

        # 3.2、获取登陆用户购物车商品
        conn = get_redis_connection('carts')
        # (1)、购物车商品数量
        # redis_carts = {b'1': b'5'}
        redis_carts = conn.hgetall('carts_%s' % user.id)
        # (2)、选中状态
        # redis_selected = [b'1']
        redis_selected = conn.smembers('selected_%s' % user.id)

        sku_ids = redis_carts.keys()  # [b'1']
        # 构建sku商品信息返回数据
        sku_list = []
        for sku_id in sku_ids:
            # sku_id = b'1'
            if sku_id in redis_selected:  # 只有被选中的sku才处理
                sku = SKU.objects.get(pk=sku_id)
                sku_list.append({
                    'id': sku.id,
                    'name': sku.name,
                    'default_image_url': sku.default_image.url,
                    'count': int(redis_carts[sku_id]),
                    'price': sku.price
                })

        # freight = 10.0 # float类型(十进制浮点数) —— 在后续计算的过程中会丢失精度
        freight = Decimal('10.0')  # Decimal类型描述的十进制数在计算的过程中可以保证精度不丢失

        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'context': {
                'addresses': address_list,
                'skus': sku_list,
                'freight': freight
            }
        })


# 提交订单(新建订单和订单商品表数据)
class OrderCommitView(LoginRequiredJSONMixin, View):

    def post(self, request):
        # 1、提取参数
        data = json.loads(request.body.decode())
        address_id = data.get('address_id')
        pay_method = data.get('pay_method')

        # 2、校验参数
        if not all([address_id, pay_method]):
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'})

        try:
            address = Address.objects.get(pk=address_id)
        except Address.DoesNotExist as e:
            return JsonResponse({'code': 400, 'errmsg': '地址不存在'})

        # OrderInfo.PAY_METHODS_ENUM.values() --> [1, 2]
        if pay_method not in [
            OrderInfo.PAY_METHODS_ENUM['CASH'],
            OrderInfo.PAY_METHODS_ENUM['ALIPAY']
        ]:
            return JsonResponse({'code': 400, 'errmsg': '支付方式不支持'})

        # 3、业务数据处理
        user = request.user
        # 约定购物车字典格式数据
        cart_dict = {}  # {1: {"count": 5, "selected": True}}
        # 获取redis购物车数据
        conn = get_redis_connection('carts')
        redis_carts = conn.hgetall('carts_%s' % user.id)  # {b'1': b'5'}
        redis_selected = conn.smembers('selected_%s' % user.id)  # [b'1']
        sku_ids = redis_carts.keys()
        for sku_id in sku_ids:
            if sku_id in redis_selected:
                cart_dict[int(sku_id)] = {
                    'count': int(redis_carts[sku_id]),
                    'selected': sku_id in redis_selected  # True
                }

        # 3.1、新建订单 —— OrderInfo
        cur_time = timezone.localtime()
        # cur_time.strftime('%Y%m%d%H%M%S') # '20201224111256'
        # order_id =  '20201224111256'  +   "00000005"
        order_id = cur_time.strftime('%Y%m%d%H%M%S') + "%08d" % user.id

        with transaction.atomic():
            # (1)、设置一个保存点 —— 用于回滚
            save_id = transaction.savepoint()
            order = OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                address=address,
                # address_id = address_id
                total_count=0,  # 初始化为0，后续统计订单商品的时候在修改
                total_amount=Decimal('0'),

                freight=Decimal('10.0'),  # 运费

                pay_method=pay_method,  # 支付方式
                # 如果用户选择支付宝，状态为未支付；如果用户选择货到付款，状态未未发货。
                status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'] if pay_method == OrderInfo.PAY_METHODS_ENUM['ALIPAY'] else
                OrderInfo.ORDER_STATUS_ENUM['UNSEND']
            )
            # 3.2、新建订单商品(就是用户redis购物车中选中的sku商品) —— OrderGoods
            sku_selected_ids = cart_dict.keys()  # 所有已经选中的商品的id
            for sku_id in sku_selected_ids:
                # sku_id是每一个被选中的sku的id
                count = cart_dict[sku_id]['count']  # 用户购买量

                while True:
                    # (1)、读取旧库存和销量数据
                    sku = SKU.objects.get(pk=sku_id)
                    old_stock = sku.stock  # 旧库存
                    old_sales = sku.sales  # 旧销量

                    # (2)、计算新库存和销量
                    new_stock = old_stock - count
                    new_sales = old_sales + count

                    # (3)、基于旧数据查找，并更新
                    # update函数返回值为一个整数表示受影响的数据条数
                    result = SKU.objects.filter(
                        pk=sku_id, stock=old_stock, sales=old_sales
                    ).update(
                        stock=new_stock, sales=new_sales
                    )
                    if result == 0:
                        # 如果result为0，说明没有数据被更新，说明filter没有过滤出任何数据，说明旧数据发生改变，说明有别的事务介入
                        continue
                    # result不为0，表示基于旧数据查找并成功更新库存和销量，针对此次sku的更新完成，跳出循环
                    break

                # TODO: 判断库存
                if count > old_stock:
                    # 库存不够 —— 下单失败
                    # (2)、回滚事务，到新建订单order之前的保存点
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'code': 400, 'errmsg': '%s,%d 库存不够' % (sku.name, sku.id)})

                # 新建OrderGoods对象保存数据库
                OrderGoods.objects.create(
                    order=order,
                    sku=sku,
                    count=count,
                    price=sku.price,  # 单价
                )

                spu = sku.spu  # 当前sku关联的spu
                spu.sales += count
                spu.save()

                # 更新订单的商品数量和总价格
                order.total_count += count
                order.total_amount += sku.price * count
            order.total_amount += order.freight  # 把运费累加到总价中
            order.save()
            # (3)、删除保存点
            transaction.savepoint_commit(save_id)

        # TODO: 清楚已经下单的购物车商品
        conn.hdel('carts_%s' % user.id, *sku_selected_ids)  # func(*[1,2]) --> func(1,2)
        conn.srem('selected_%s' % user.id, *sku_selected_ids)

        # 4、构建响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'order_id': order_id})
