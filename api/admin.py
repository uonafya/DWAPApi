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


class ComparisonAdmin(admin.ModelAdmin):
    search_fields = ('facility', 'ward', 'subcounty', 'county',
                     'indicators', 'khis_minus_datim', 'concodance')
    list_filter = ['created', 'county', 'facility', 'ward',
                   'subcounty']
    list_display = ['facility', 'ward', 'subcounty', 'county', 'MOH_FacilityID', 'MOH_IndicatorCode', 'DATIM_Disag_Name',
                    'indicators', 'khis_data', 'datim_data', 'weight', 'concodance', 'khis_minus_datim']


class CountyAdmin(admin.ModelAdmin):
    search_fields = ('county_name',)
    list_filter = ['county_name', ]
    list_display = ['county_name', ]


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category_name',)
    list_filter = ['category_name', ]
    list_display = ['category_name', ]


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
admin.site.register(final_comparison_data, ComparisonAdmin)
admin.site.register(counties, CountyAdmin)
admin.site.register(indicator_category, CategoryAdmin)
