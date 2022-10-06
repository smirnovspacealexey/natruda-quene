# -*- coding: utf-8 -*-

from .models import Menu, Staff, Order, StaffCategory, \
    MenuCategory, Servery, ServicePoint, Printer, CallData, Customer, Delivery, DeliveryOrder, ServiceAreaPolygon, \
    ServiceAreaPolyCoord, MacroProduct, MacroProductContent, ProductOption, ProductVariant, SizeOption, ContentOption, \
    Server1C
from django.contrib import admin


def accepted_everything(modeladmin, request, queryset):
    CallData.objects.filter(accepted=False).update(accepted=True)


# Register your models here.
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer_title', 'note', 'price', 'guid_1c', 'category']
    search_fields = ['title', 'guid_1c', ]
    list_editable = ('customer_title', 'category', )


@admin.register(Servery)
class ServeryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'display_title', 'ip_address', 'guid_1c', 'service_point', 'payment_kiosk', 'default_remote_order_acceptor']
    search_fields = ['display_title', 'title', 'guid_1c', ]
    list_editable = ('ip_address', 'guid_1c', 'service_point', 'payment_kiosk', 'default_remote_order_acceptor')


@admin.register(CallData)
class CallDataAdmin(admin.ModelAdmin):
    list_display = ['customer', 'call_manager', 'ats_id', 'timepoint', 'duration', 'record', 'accepted', 'missed']
    search_fields = ['customer__phone_number', 'customer__name', 'customer__email', 'ats_id', ]
    list_filter = ['accepted', 'missed', ]
    actions = [accepted_everything, ]

admin.site.register(Staff)
admin.site.register(Order)
admin.site.register(StaffCategory)
admin.site.register(MenuCategory)
admin.site.register(ServicePoint)
admin.site.register(Printer)
admin.site.register(Customer)
admin.site.register(Delivery)
admin.site.register(DeliveryOrder)
admin.site.register(ServiceAreaPolygon)
admin.site.register(ServiceAreaPolyCoord)
admin.site.register(MacroProduct)
admin.site.register(MacroProductContent)
admin.site.register(ProductOption)
admin.site.register(ProductVariant)
admin.site.register(SizeOption)
admin.site.register(ContentOption)
admin.site.register(Server1C)
