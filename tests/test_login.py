from django.test import TestCase, Client
from core.models.auth import UserInfo

from django.contrib.auth.hashers import make_password, check_password


class TestLoginView(TestCase):
    """
    用于测试用户登录页面
    """

    def setUp(self):
        # 创建一个测试用户
        self.user = UserInfo.objects.update_or_create(name="testUser",
                                                      password=make_password('testPassword', salt='Wocater'))

    def test_model(self):
        """
        测试数据库
        :return: None
        """
        # 测试获取用户名
        self.assertEqual((data := UserInfo.objects.get(name='testUser')).name, 'testUser')
        # 验证密码
        self.assertTrue(check_password('testPassword', data.password))

    def test_get(self) -> None:
        """
        测试Get方法
        :return: None
        """
        client = Client()
        response = client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_post(self) -> None:
        """
        测试Post提交表单
        :return: None
        """
        self.maxDiff = None
        client = Client()
        response = client.post("/login/", data={'name': 'testUser', 'password': 'testPassword'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'error': False})
