from django_redis import get_redis_connection
from meiduo_mall.utils.cookiesecret import CookieSecret


# 功能：合并cookie购物车到redis中
# 参数：request请求对象用于获取cookie购物车数据；response响应对象用于请求cookie购物车
# 返回值：响应对象
def merge_cart_cookie_to_redis(request, response):
    # 1、提取cookie购物车数据
    cookie_str = request.COOKIES.get('carts')
    if cookie_str:
        cart_dict = CookieSecret.loads(cookie_str)
    else:
        cart_dict = {}

    # 2、把cookie购物车数据合并到redis中
    conn = get_redis_connection('carts')
    # (1)、商品数量
    # conn.hincryby() --> 该函数是累加数量，我们在合并采用覆盖原则写入
    # conn.hset() --> 采用hset函数，redis存在则直接覆盖，不存在则直接新增
    # (2)、选中状态
    # conn.sadd()插入集合，conn.srem()从集合中去除 —— 如果商品id不再集合中，不会出异常

    user = request.user
    # cart_dict = {1: {"count": 5, "selected": True}}
    sku_ids = cart_dict.keys()  # [1,2....]
    for sku_id in sku_ids:
        conn.hset('carts_%s' % user.id, sku_id, cart_dict[sku_id]['count'])
        selected = cart_dict[sku_id]['selected']
        if selected:
            conn.sadd('selected_%s' % user.id, sku_id)
        else:
            conn.srem('selected_%s' % user.id, sku_id)

    # 3、清除cookie中到购物车
    response.delete_cookie('carts')
    return response
