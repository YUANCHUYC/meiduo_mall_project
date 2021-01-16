"""
用于自定义分页器模块
"""
# 自定义一个分页器
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MyPage(PageNumberPagination):
    page_query_param = 'page'  # ?page=1
    page_size_query_param = 'pagesize'  # ?pagesize=10
    max_page_size = 100  # 最大每页按照100个划分
    page_size = 10  # 默认按照10个每页划分

    # 重写
    def get_paginated_response(self, data):
        # 功能：构建一个响应对象（封装响应参数）
        # 参数：data --> 当前页数据
        return Response({
            'counts': self.page.paginator.count,
            'lists': data,
            'page': self.page.number,
            'pages': self.page.paginator.num_pages,
            'pagesize': self.page_size  # 后端默认每页数量
        })
