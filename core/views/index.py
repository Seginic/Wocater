from django.core.handlers.wsgi import WSGIRequest
from django.views import View
from django.shortcuts import render, redirect


class IndexView(View):
    def get(self, request: WSGIRequest, *args, **kwargs):
        """
        处理主页面的页面请求
        :param request: Get请求
        :param args: 额外的参数
        :param kwargs: 额外的关键字参数
        :return: 返回Http视图
        """
        # 判断用户是否登录
        # session键为'hasLoggedIn'
        if not request.session.get('hasLoggedIn', False):
            # 如果没有登录
            # 重定向到登录页
            return redirect('/login/', permanent=True)
