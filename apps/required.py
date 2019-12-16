from django.http import HttpResponseRedirect
from django.http import JsonResponse
from user.models import MyLog
from my_const import *


def operate_data_required(right=None):
    def check(function=None):
        def filter(request):
            try:
                MyLog.objects.log_action(request, CATEGORY_OPERATE, ACTION_OTHER)
                request.user.right_operate.index(right)
                return function(request)
            except:
                return JsonResponse({"success": False})

        return filter

    return check


def operate_url_required(right=None):
    def check(function=None):
        def filter(request):
            try:
                request.user.right_operate.index(right)
                return function(request)
            except:
                return HttpResponseRedirect('/home/')

        return filter

    return check


def backup_data_required(right=None):
    def check(function=None):
        def filter(request):
            try:
                MyLog.objects.log_action(request, CATEGORY_BACKUP, ACTION_SEARCH)
                request.user.right_backup.index(right)
                return function(request)
            except:
                return JsonResponse({"success": False})

        return filter

    return check


def top_data_required(right=None):
    def check(function=None):
        def filter(request):
            try:
                MyLog.objects.log_action(request, CATEGORY_TOP, ACTION_SEARCH)
                request.user.right_top.index(right)
                return function(request)
            except:
                return JsonResponse({"success": False})

        return filter

    return check


def price_data_required(right=None):
    def check(function=None):
        def filter(request):
            try:
                MyLog.objects.log_action(request, CATEGORY_PRICE, ACTION_SEARCH)
                request.user.right_price.index(right)
                return function(request)
            except:
                return JsonResponse({"success": False})

        return filter

    return check


def task_data_required(right=None):
    def check(function=None):
        def filter(request):
            try:
                request.user.right_task.index(right)
                return function(request)
            except:
                return JsonResponse({"success": False})

        return filter

    return check


def sale_data_required(right=None):
    def check(function=None):
        def filter(request):
            try:
                MyLog.objects.log_action(request, CATEGORY_SALE, ACTION_SEARCH)
                request.user.right_sale.index(right)
                return function(request)
            except:
                return JsonResponse({"success": False})

        return filter

    return check


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
