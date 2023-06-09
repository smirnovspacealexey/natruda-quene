from django.contrib import admin
from .models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name', 'logg', 'datetime']
    list_editable = ('name',)
    search_fields = ['name', ]
    list_filter = ['datetime', ]




