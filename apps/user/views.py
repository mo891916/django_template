import logging

from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import View

from .forms import LoginForm
from .models import MyLog
from my_const import ACTION_LOGIN_IN, ACTION_LOGIN_OUT, CATEGORY_USER


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            account = request.POST.get('username')
            pwd = request.POST.get('password')
            # 日志记录
            MyLog.objects.log_action(request, CATEGORY_USER, ACTION_LOGIN_IN, f'{account}登录')
            user = authenticate(username=account, password=pwd)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/home/')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


def logout_view(request):
    MyLog.objects.log_action(request, CATEGORY_USER, ACTION_LOGIN_OUT, '退出系统')
    logout(request)
    return render(request, 'login.html')


@login_required
def index(request):
    return render_to_response('index.html')


def page_not_found(request, exception=None):
    return render_to_response('404.html')


def page_error(request, exception=None):
    return render_to_response('500.html')
