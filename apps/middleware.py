from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import logging

logger = logging.getLogger('log_request')


class CustomAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request_path = request.path
        if not request_path.startswith('/static') and not request_path.startswith('/favicon'):
            method = request.method
            if method == 'GET':
                content = str(request.GET)
            elif method == 'POST':
                content = str(request.POST)
            else:
                content = request.META['QUERY_STRING']
            logger.info(
                str({'from_ip': request.META['REMOTE_ADDR'], 'user_name': request.user.username, 'method': method,
                     'path': request_path, 'query_content': content}))
        if request_path.startswith('/client') or request_path.startswith('/note') or request_path.startswith('/home'):
            if not request.user.is_authenticated:
                return HttpResponseRedirect(settings.LOGIN_URL)
        # if request_path.startswith('/client'):
        #     if   illegality:
        #         return HttpResponseRedirect(settings.LOGIN_URL)
