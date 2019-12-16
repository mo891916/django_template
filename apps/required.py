from django.http import HttpResponseRedirect
from django.http import JsonResponse
from user.models import MyLog
from my_const import *





def client_data_required(right=None):
    def check(function=None):
        def filter(request):
            try:
                MyLog.objects.log_action(request, CATEGORY_INFO, ACTION_SEARCH)
                request.user.right_client.index(right)
                return function(request)
            except:
                return JsonResponse({"success": False})

        return filter

    return check


def client_url_required(right=None):
    def check(function=None):
        def filter(request):
            try:
                request.user.right_client.index(right)
                return function(request)
            except:
                return HttpResponseRedirect('/home/')

        return filter

    return check
