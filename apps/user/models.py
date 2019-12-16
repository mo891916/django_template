from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    gender = models.CharField(max_length=6, verbose_name='性别', choices=(('male', '男'), ('female', '女')),
                              default='female')
    address = models.CharField(max_length=100, verbose_name='地址', default='')
    mobile = models.CharField(max_length=11, verbose_name='手机号', null=True, blank=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户组'

    def __str__(self):
        return self.username
