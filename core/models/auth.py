from django.db import models


class UserInfo(models.Model):
    name = models.CharField(max_length=16, verbose_name='用户名')
    # 明文密码最长20 加密后最长长度73 盐为Wocater
    # 这里设置最长长度为75
    password = models.CharField(max_length=75, verbose_name='密码')

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
