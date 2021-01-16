"""
当前home_views模块用于定义主页数据统计接口视图
"""

from datetime import timedelta
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from users.models import User
from orders.models import OrderInfo


# 用户总数
class UserTotalCountView(APIView):
    permission_classes = [IsAdminUser]  # 当前视图接口只有is_staff=True才能访问

    def get(self, request):
        # 1、统计出注册的用户总数量
        count = User.objects.count()
        # 当前时刻
        # timezone.localtime()返回值是django工程配置中设定的时区的当前时刻datetime对象
        cur_time = timezone.localtime()  # 2021-1-8 10:11:23 +08:00 Asia/Shanghai
        timezone.now()
        print("cur_time: ", cur_time)
        # 2、构建响应参数返回
        return Response({
            'count': count,
            # cur_time.date(): 2021-1-8
            'date': cur_time.date()  # 把datetime对象转化为date对象(只保留年月日)
        })


# 日增用户统计
class UserDayCountView(APIView):

    def get(self, request):
        # 需求：统计当日新建的用户 —— 模型类过滤统计
        # 明确：已知条件(当日的0时刻)，过滤逻辑(用户新建时间大于等于当日0时刻)
        # 1、获取当日的0时刻
        cur_time = timezone.localtime()  # 2021-1-8 10:37:34 +08:00
        cur_0_time = cur_time.replace(hour=0, minute=0, second=0)  # 2021-1-8 00:00:00 +08:00
        # 2、过滤统计
        count = User.objects.filter(
            date_joined__gte=cur_0_time
        ).count()

        return Response({
            'count': count,
            'date': cur_0_time.date()
        })


# 日活跃用户
class UserActiveCountView(APIView):

    def get(self, request):
        cur_time = timezone.localtime()
        cur_0_time = cur_time.replace(
            hour=0,
            minute=0,
            second=0
        )

        count = User.objects.filter(
            last_login__gte=cur_0_time
        ).count()

        return Response({
            'count': count,
            'date': cur_0_time.date()
        })


# 日下单用户数量统计
class UserOrderCountView(APIView):

    def get(self, request):
        # 需求：统计当日下了的订单关联用户的数量
        # (1)、已知条件(订单的条件，从表已知条件)：当日的零时刻
        # (2)、目标数据(用户数据，主表数据)：用户数量
        # 总结：使用从表的已知条件，过滤出主表目标数据

        # 1、获取已知条件：当日零时刻
        cur_time = timezone.localtime()
        cur_0_time = cur_time.replace(
            hour=0,
            minute=0,
            second=0
        )
        # 2、过滤查询
        # 方案一：从从表入手查询
        orders = OrderInfo.objects.filter(
            create_time__gte=cur_0_time
        )
        user_set = set() # 实例化一个集合对象
        for order in orders:
            user = order.user # 当前订单关联的用户
            user_set.add(user) # 集合插入自动去重
        count = len(user_set)

        # 方案二：从主表入手查询
        # users = User.objects.filter(
        #     # 如何使用从表的已知条件过滤主表数据
        #     orders__create_time__gte=cur_0_time
        # )
        # count = len(set(users))
        #
        return Response({
            'count': count,
            'date': cur_0_time.date()
        })


# 月增用户注册数量统计：包括当日在内的最近30天其中每一天注册用户数量
class UserMonthCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 1、获取当日的0时刻
        cur_time = timezone.localtime()
        # 当日0时刻(也是30天中最后一天的0时刻)：2021-1-8 0:0:0 +8:00
        end_0_time = cur_time.replace(hour=0, minute=0, second=0)
        # 2、起始日期的0时刻
        # start_0_time =  end_0_time  -  (统计天数 - 1)
        start_0_time = end_0_time - timedelta(days=29)
        # 3、从起始时间start_0_time遍历获取30天中的每一天的0时刻用于统计
        data = []
        for index in range(30):
            # calc_0_time = start_0_time + timedelta(days=0)   index=0
            # calc_0_time = start_0_time + timedelta(days=1)   index=1
            # calc_0_time = start_0_time + timedelta(days=2)   index=2
            # .......
            # calc_0_time = start_0_time + timedelta(days=29)  index=29
            # 公式：calc_0_time = start_0_time + timedelta(days=index)
            # 其中某一天的用于计算的0时刻
            calc_0_time = start_0_time + timedelta(days=index)
            # 次日的0时刻
            #  2021-1-6 0:0:0 +8:00  =  2021-1-5 0:0:0 +8:00 + 1天
            next_0_time = calc_0_time + timedelta(days=1)

            count = User.objects.filter(
                date_joined__gte=calc_0_time,  # 大于等于某一天的0时刻
                date_joined__lt=next_0_time  # 小于次日的0时刻
            ).count()

            data.append({
                'count': count,
                'date': calc_0_time.date()
            })

        return Response(data)
