from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from .models import UserProfile
from .forms import LoginForm
import logging

logger = logging.getLogger('user.views')


class LoginView(View):
    def get(self, request):
        logger.info('--------------login----------------')
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            account = request.POST.get('username')
            pwd = request.POST.get('password')
            print('{0},{1}'.format(account, pwd))
            user = authenticate(username=account, password=pwd)
            if user:
                if user.is_active:
                    login(request, user)
                    # return render(request, 'index.html')
                    return HttpResponseRedirect('/home/')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


def logout_view(request):
    logout(request)
    return render(request, 'login.html')


@login_required
def index(request):
    return render_to_response('index.html')
