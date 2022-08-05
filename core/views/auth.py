from django.contrib.auth.hashers import check_password
from django.core.handlers.wsgi import WSGIRequest
from django.views import View
from django.shortcuts import render, redirect

from core.forms.login import LoginForm
from core.models.auth import UserInfo


class LoginView(View):
    """
    用于处理登录页面的视图类
    """

    def get(self, request: WSGIRequest, *args, **kwargs):
        """
        用于处理用户登录时的页面请求
        :param request: Get请求
        :param args: 额外的参数
        :param kwargs: 额外的关键字参数
        :return: 返回Http视图
        """
        # 检测用户是否登录
        # session键为'hasLoggedIn'
        if request.session.get('hasLoggedIn', False):
            # 重定向到主页
            return redirect('/', permanent=True)
        return render(request, 'Tinydash/auth-login.html')

    def post(self, request: WSGIRequest, *args, **kwargs):
        """
        用于处理用户登录时提交的表单
        :param request: Post请求
        :param args: 额外的参数
        :param kwargs: 额外的关键字参数
        :return: 返回Http视图
        """
        # TODO: 使用ajax代替表单传值
        # 使用Form类解析表单
        login_form = LoginForm(request.POST)
        # 判断表单是否有效
        from django.http import HttpResponse
        if login_form.is_valid():
            # 表单有效
            # 获取表单中的用户名、密码、是否记录登录状态等信息
            name, password = (cleaned_data := login_form.cleaned_data).get('name'), cleaned_data.get('password')
            try:
                # 检查密码是否匹配
                # 先在数据库中查询到用户名所对的密码（加密状态），再用用户提供的明文密码进行验证
                if check_password(password, UserInfo.objects.get(name=name).password):
                    # 密码验证通过
                    # 更新用户的session
                    response = redirect('/', permanent=True)
                    response.session['hasLoggedIn'] = True
                    return response
                else:
                    # 密码验证未通过
                    # 向前端返回错误信息
                    # TODO
                    return HttpResponse('false')
            except (UserInfo.DoesNotExist, UserInfo.MultipleObjectsReturned):
                return HttpResponse('error')
        else:
            return HttpResponse('not valid')
