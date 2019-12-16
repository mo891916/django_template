from datetime import datetime

from django.contrib import admin
from django.utils.encoding import escape_uri_path
from import_export import resources
from import_export.admin import ExportMixin
from import_export.formats.base_formats import XLS, XLSX, HTML

from .models import MyLog
from .models import UserProfile

admin.site.register(UserProfile)


class MyLogAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    list_display = ('id', 'action_time', 'user', 'category', 'action_flag', 'ip', 'request_url', 'message')
    search_fields = ('request_url','message')
    list_filter = ('user', 'category', 'action_flag', 'ip')


admin.site.register(MyLog, MyLogAdmin)

admin.site.site_title = "稽核后台"
admin.site.site_header = "稽核后台"


class ExportModelAdmin(ExportMixin, admin.ModelAdmin):
    # in Version 1.2
    # def get_export_filename(self, file_format):
    #     date_str = datetime.now().strftime('%Y-%m-%d')
    #     filename = "%s-%s.%s" % (escape_uri_path(self.model._meta.verbose_name),
    #                              date_str,
    #                              file_format.get_extension())
    #     return filename
    formats = (XLS, XLSX, HTML)

    def get_export_filename(self, request, queryset=None, file_format=None):
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = "%s-%s.%s" % (escape_uri_path(self.model._meta.verbose_name),
                                 date_str,
                                 file_format.get_extension())

        return filename


class MyModelResource(resources.ModelResource):
    def __init__(self):
        self.fields_verbose_name = {}
        for i in self.Meta.model._meta.fields:
            if i.related_model:
                for j in i.related_model._meta.fields:
                    self.fields_verbose_name[i.name + '__' + j.name] = j.verbose_name
            self.fields_verbose_name[i.name] = i.verbose_name

    def get_export_headers(self):
        headers = []
        for field in self.get_export_fields():
            try:
                headers.append(self.fields_verbose_name[field.column_name])
            except:
                headers.append(field.column_name)
        return headers
