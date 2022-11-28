from django.contrib import admin
from .models import ExcelBase
from .backend import excel_to_base


def parse_to_base(modeladmin, request, queryset):
    excel_base = queryset.first()
    excel_to_base(excel_base.excel.path)


parse_to_base.short_description = 'отпарсить в базу'


@admin.register(ExcelBase)
class ExcelBaseAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name', 'excel', ]
    list_editable = ('name', 'excel')
    search_fields = ['name', ]
    actions = [parse_to_base, ]


