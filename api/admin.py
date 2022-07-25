from django.contrib import admin
from .models import *
# Register your models here.


class IndicatorAdmin(admin.ModelAdmin):
    search_fields = ('name', 'id', 'created', 'lastUpdated', 'displayName')


class indicatorTypeAdmin(admin.ModelAdmin):
    search_fields = ('name', 'id')


class indicatorGroupsAdmin(admin.ModelAdmin):
    search_fields = ('name', 'id', 'created', 'lastUpdated')


admin.site.register(indicators, IndicatorAdmin)
admin.site.register(indicatorType, indicatorTypeAdmin)
admin.site.register(indicatorGroups, indicatorGroupsAdmin)
admin.site.register(middleware_settings)
admin.site.register(total_records)
admin.site.register(schedule_settings)
admin.site.register(Data_Mapping_Files)
