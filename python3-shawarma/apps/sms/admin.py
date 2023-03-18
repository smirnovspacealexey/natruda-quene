from django.contrib import admin
from .models import MangoSettings, SMSHistory
from time import gmtime, strftime


def send_test_sms(modeladmin, request, queryset):
    from .mango import send_sms
    for mango_settings in queryset:
        send_sms(mango_settings.test_phone,
                 f'TEST SMS {strftime("%d-%m-%Y %H:%M:%S", gmtime())}', 'test',
                 mango_settings.vpbx_api_key, mango_settings.vpbx_api_salt, mango_settings.from_extension)


send_test_sms.short_description = 'отправить тестовую СМС'


def resend_sms(modeladmin, request, queryset):
    from .backend import send_sms
    for sms in queryset:
        send_sms(sms.phone, sms.text)


resend_sms.short_description = 'повторно отправить смс'


@admin.register(MangoSettings)
class MangoSettingsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'vpbx_api_key', 'vpbx_api_salt', 'from_extension', 'active']
    list_editable = ('vpbx_api_key', 'vpbx_api_salt', 'from_extension', 'active')
    search_fields = ['name', ]
    actions = [send_test_sms, ]


@admin.register(SMSHistory)
class SMSHistoryAdmin(admin.ModelAdmin):
    list_display = ['phone', 'text', 'success', 'result', 'date']
    search_fields = ['phone', 'text', 'success', 'result', 'date']
    actions = [resend_sms, ]


