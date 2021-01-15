"""
自定义一个判断用户登陆的拓展视图类
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class LoginRequiredJSONMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        # 默认该函数返回的是一个重定向响应对象HttpResponseRedirect
        # 我们为了和美多商城工程一致，需要返回一个JsonResponse
        return JsonResponse({'code': 400, 'errmsg': '未登陆'})
