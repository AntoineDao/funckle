from typing import Any
from django.contrib import admin

from .models import Function, FunctionVersion


class FunctionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')


class FunctionVersionAdmin(admin.ModelAdmin):
    list_display = ('function', 'version', 'status',
                    'created_at', 'updated_at')


admin.site.register(Function, FunctionAdmin)
admin.site.register(FunctionVersion, FunctionVersionAdmin)
