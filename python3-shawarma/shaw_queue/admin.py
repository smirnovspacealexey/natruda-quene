# -*- coding: utf-8 -*-

from .models import Menu, Staff, Order, StaffCategory, \
    MenuCategory, Servery, ServicePoint, Printer, CallData, Customer, Delivery, DeliveryOrder, ServiceAreaPolygon, \
    ServiceAreaPolyCoord, MacroProduct, MacroProductContent, ProductOption, ProductVariant, SizeOption, ContentOption, \
    Server1C, CookingTime, OrderContent, CookingTimerOrderContent
from django.contrib import admin
from apps.delivery.backend import delivery_request
from django import forms


def accepted_everything(modeladmin, request, queryset):
    CallData.objects.filter(accepted=False).update(accepted=True)

accepted_everything.short_description = 'завершить все звонки'


def testdelivery(modeladmin, request, queryset):
    from apps.delivery.models import YandexSettings
    yandex_settings = YandexSettings.current()
    destination = {
                    "fullname": "Челябинск, Университетская Набережная 63",
                    "building": "63",
                    # "building_name": "Alex",
                    "city": "Челябинск",
                    "comment": "ТЕСТОВЫЙ ЗАКАЗ НЕ ВЫПОЛНЯТЬ. ТЕСТИРУЕМ АПИ",
                    "country": "Россия",
                    "description": "Челябинск, Россия",
                    "door_code": "",
                    "door_code_extra": "",
                    "doorbell_name": "",
                    "porch": "1",
                    "sflat": "1",
                    "sfloor": "1",

                    "email": '',
                    "name": 'Alex',
                    "phone": yandex_settings.test_phone,

    }
    delivery_request(Order.objects.last(), queryset, destination)


testdelivery.short_description = 'сделать тестовый заказ'


# Register your models here.
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer_title', 'note', 'price', 'guid_1c', 'category', 'get_cooking_time', 'QR_required']
    search_fields = ['title', 'guid_1c', ]
    list_editable = ('customer_title', 'category', 'QR_required')

    Menu.get_cooking_time.short_description = 'время готовки'


@admin.register(Servery)
class ServeryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'display_title', 'ip_address', 'guid_1c', 'service_point', 'payment_kiosk', 'default_remote_order_acceptor']
    search_fields = ['display_title', 'title', 'guid_1c', ]
    list_editable = ('ip_address', 'guid_1c', 'service_point', 'payment_kiosk', 'default_remote_order_acceptor')


@admin.register(CallData)
class CallDataAdmin(admin.ModelAdmin):
    list_display = ['customer', 'call_manager', 'ats_id', 'timepoint', 'accepted', 'missed', 'duration', 'record']
    search_fields = ['customer__phone_number', 'customer__name', 'customer__email', 'ats_id', ]
    list_filter = ['accepted', 'missed', ]
    actions = [accepted_everything, ]


class OrderContentInline(admin.TabularInline):
    model = OrderContent
    extra = 0

    fieldsets = (
        (None, {
            # 'fields': ('menu_item', 'note', 'quantity', 'info'),
            'fields': ('info', ),
        }),
    )
    readonly_fields = ('info',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'daily_number', 'open_time', 'close_time', 'content_completed', 'is_paid', 'is_delivery', 'from_site', 'guid_1c']
    search_fields = ['daily_number', ]
    list_filter = ['from_site', 'is_delivery', 'is_paid']
    inlines = [OrderContentInline]


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer_title', 'menu_item',]
    search_fields = ['title', 'customer_title']
    filter_horizontal = ('product_variants', )


@admin.register(CookingTime)
class CookingTimeAdmin(admin.ModelAdmin):
    list_display = ['minutes', 'quantity_products', 'quantity_categories', 'default']
    list_editable = ('default', )
    search_fields = ['minutes', ]
    filter_horizontal = ()


@admin.register(DeliveryOrder)
class DeliveryOrderAdmin(admin.ModelAdmin):
    list_display = ['order', 'daily_number', 'address', 'obtain_timepoint', 'note', 'moderation_needed', 'is_ready', 'is_delivered']
    list_editable = ('note', 'moderation_needed')
    search_fields = ['note', 'address']
    raw_id_fields = ["order", 'customer']


@admin.register(MacroProductContent)
class MacroProductContentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'menu_title', 'customer_title', 'customer_appropriate']
    list_editable = ('title', 'customer_appropriate')
    search_fields = ['title', 'menu_title', 'customer_title']


@admin.register(ServicePoint)
class ServicePointAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'fullname', 'latitude', 'longitude']
    list_editable = ('title', 'fullname', 'latitude', 'longitude')
    search_fields = ['title', 'fullname']
    actions = [testdelivery, ]

admin.site.register(Staff)
admin.site.register(StaffCategory)
admin.site.register(MenuCategory)
admin.site.register(Printer)
admin.site.register(Customer)
admin.site.register(Delivery)
admin.site.register(ServiceAreaPolygon)
admin.site.register(ServiceAreaPolyCoord)
admin.site.register(MacroProduct)
admin.site.register(ProductVariant)
admin.site.register(SizeOption)
admin.site.register(ContentOption)
admin.site.register(Server1C)
admin.site.register(CookingTimerOrderContent)
# admin.site.register(OrderContent)
