from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect

# 国际化和本地化支持
from django.utils.translation import gettext as _

from core.forms.auth import LoginForm
from core.models.auth import UserInfo


class LoginView(View):
    """
    用于处理登录页面的视图类
    """

    @staticmethod
    def get(request, *args, **kwargs):
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
        # 返回渲染页面
        return render(request, 'Tinydash/auth-login.html', {'error_text': _('Incorrect username or password.')})

    @staticmethod
    def post(request, *args, **kwargs):
        """
        用于处理用户登录时提交的表单
        :param request: Post请求
        :param args: 额外的参数
        :param kwargs: 额外的关键字参数
        :return: 返回Http视图
        """
        # 使用Form类解析表单
        login_form = LoginForm(request.POST)
        # 判断表单是否有效
        if login_form.is_valid():
            # 表单有效
            # 获取表单中的用户名、密码、是否记录登录状态等信息
            name, password, remember_user = (cleaned_data := login_form.cleaned_data).get('name'), cleaned_data.get(
                'password'), cleaned_data.get('remember_me')
            try:
                # 检查密码是否匹配
                # 先在数据库中查询到用户名所对的密码（加密状态），再用用户提供的明文密码进行验证
                if check_password(password, UserInfo.objects.get(name=name).password):
                    # 密码验证通过
                    # 设置session
                    request.session['hasLoggedIn'] = True
                    if remember_user:
                        # 设置session过期时间为 关闭浏览器后立即过期
                        request.session.set_expiry(0)
                    return JsonResponse({'error': False})
            except UserInfo.DoesNotExist:
                pass

        # 无论不存在用户 还是用户密码错误 统一返回
        return JsonResponse({'error': True})
