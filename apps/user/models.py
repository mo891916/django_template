import json

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http.request import QueryDict

from .fields import IntegerRangeField


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    gender = models.CharField(max_length=6, verbose_name='性别', choices=(('male', '男'), ('female', '女')),
                              default='female')
    department = models.CharField(max_length=100, verbose_name='部门', default='', blank=True)
    mobile = models.CharField(max_length=11, verbose_name='手机号', null=True, blank=True)
    permission = IntegerRangeField(min_value=0, max_value=10, null=True, verbose_name='权限0-10', default=0)
    right_client = models.CharField(max_length=26, default='', null=True, blank=True, verbose_name='顾客列表查看权限')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户组'

    def __str__(self):
        return f"{self.nick_name}"


class MyLogEntryManager(models.Manager):
    use_in_migrations = True

    def log_action(self, request, category, action_flag, message=None):
        """
        添加日志
        :param request: 请求
        :param category: 操作类别
        :param action_flag: 操作类型
        :param message: 内容
        :return:
        """
        method = request.method
        if not message:
            if method == 'GET':
                message = request.GET
            elif method == 'POST':
                message = request.POST
            else:
                message = request.META['QUERY_STRING']
        if isinstance(message, QueryDict) or isinstance(message, dict):
            message = dict(message)
            content = {}
            for i in message:
                if i != 'csrfmiddlewaretoken' and i != '_':
                    content[i] = message[i]
            message = json.dumps(content, ensure_ascii=False)

        return self.model.objects.create(
            user_id=request.user.pk if request.user.pk is not None else -1,
            category=category,
            action_flag=action_flag,
            message=message[:250],
            ip=request.META['REMOTE_ADDR'],
            request_url=request.path,
            request_method=method
        )


class MyLog(models.Model):
    action_time = models.DateTimeField(auto_now_add=True, editable=False,
                                       verbose_name='操作时间')  # default=timezone.now,
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name="操作人", default=-1)
    category = models.IntegerField(
        choices=[(0, '其他'), (1, '用户'), (2, '会员'), (3, '特殊操作'), (4, '邮件发送')], verbose_name="内容类别")
    action_flag = models.IntegerField(
        choices=[(0, '其他'), (1, '添加'), (2, '修改'), (3, '删除'), (4, '查询'), (5, '登录'), (6, '登出'), (7, '任务计划')],
        verbose_name="操作类型")
    message = models.CharField(blank=True, verbose_name="内容", default="", max_length=260)
    ip = models.CharField(max_length=16, default='0.0.0.0', null=True, blank=True, verbose_name='IP地址')
    request_url = models.CharField(max_length=100, null=True, verbose_name='请求链接')
    request_method = models.CharField(max_length=30, blank=True, verbose_name='请求方式')

    objects = MyLogEntryManager()

    class Meta:
        verbose_name = '操作日志'
        verbose_name_plural = '用户操作日志'
