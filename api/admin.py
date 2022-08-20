from django.contrib import admin
from .models import *
# Register your models here.


class IndicatorAdmin(admin.ModelAdmin):
    search_fields = ('MOH_Indicator_ID', 'MOH_Indicator_Name', 'created',
                     'lastUpdated', 'displayName')
    list_filter = ['created',
                   'lastUpdated', 'MOH_Indicator_Name', 'MOH_Indicator_ID']
    list_display = ['MOH_Indicator_Name',
                    'MOH_Indicator_ID', 'created', 'lastUpdated']


class MappingAdmin(admin.ModelAdmin):
    search_fields = ('DATIM_Indicator_Category', 'DATIM_Disag_Name',
                     'MOH_Indicator_Name', 'Operation', 'MOH_Indicator_ID')
    list_filter = ['DATIM_Indicator_Category', 'DATIM_Disag_Name',
                   'MOH_Indicator_Name', 'Operation', 'MOH_Indicator_ID']
    list_display = ['DATIM_Indicator_Category', 'Operation', 'DATIM_Disag_Name',
                    'MOH_Indicator_Name',  'MOH_Indicator_ID']


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
admin.site.register(mapped_data, MappingAdmin)
