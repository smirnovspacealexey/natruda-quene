from django.contrib import admin
from .models import YandexSettings
from time import gmtime, strftime


@admin.register(YandexSettings)
class YandexSettingsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'token', 'active']
    list_editable = ('token', 'active')
    search_fields = ['__str__', ]



