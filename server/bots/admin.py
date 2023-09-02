from django.contrib import admin

from .models import Stream, Bot


class StreamAdmin(admin.ModelAdmin):
    list_display = ('speckle_id', 'name')


class BotAdmin(admin.ModelAdmin):
    list_display = ('owner', 'slug', 'description', 'stream',
                    'webhook_id', 'function_version')


admin.site.register(Stream, StreamAdmin)
admin.site.register(Bot, BotAdmin)
