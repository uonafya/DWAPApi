from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(indicators)
class IndicatorAdmin(admin.ModelAdmin):
    search_fields = ('MOH_Indicator_ID', 'MOH_Indicator_Name', 'created',
                     'lastUpdated', 'displayName')
    list_filter = ['created',
                   'lastUpdated', 'MOH_Indicator_Name', 'MOH_Indicator_ID']
    list_display = ['MOH_Indicator_Name',
                    'MOH_Indicator_ID', 'created', 'lastUpdated']

@admin.register(mapped_data)
class MappingAdmin(admin.ModelAdmin):
    search_fields = ('DATIM_Indicator_Category', 'DATIM_Disag_Name',
                     'MOH_Indicator_Name', 'Operation', 'MOH_Indicator_ID')
    list_filter = ['DATIM_Indicator_Category', 'DATIM_Disag_Name',
                   'MOH_Indicator_Name', 'Operation', 'MOH_Indicator_ID']
    list_display = ['DATIM_Indicator_Category', 'Operation', 'DATIM_Disag_Name',
                    'MOH_Indicator_Name',  'MOH_Indicator_ID']

@admin.register(final_comparison_data)
class ComparisonAdmin(admin.ModelAdmin):
    search_fields = ('facility',  'category', 'ward', 'subcounty', 'county',
                     'indicators', 'khis_minus_datim', 'concodance', 'weight','DATIM_Disag_Name',)
    list_filter = ['create_date', 'county',  'category', 'facility', 'ward',
                   'subcounty', 'concodance', 'weight']
    list_display = ['category', 'facility', 'ward', 'subcounty', 'county', 'MOH_FacilityID', 'MOH_IndicatorCode', 'DATIM_Disag_Name',
                    'indicators', 'khis_data', 'datim_data', 'khis_minus_datim', 'weight', 'concodance']

@admin.register(counties)
class CountyAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ['name', ]
    list_display = ['name', ]

@admin.register(subcounties)
class SubCountyAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ['name', ]
    list_display = ['name', ]

@admin.register(ward)
class WardAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ['name', ]
    list_display = ['name', ]

@admin.register(Facilities)
class FacilitiesAdmin(admin.ModelAdmin):
    search_fields = ('name','uid','mfl_code','level')
    list_filter = ['name','uid','mfl_code','level' ]
    list_display = ['name','uid','mfl_code','level' ]

@admin.register(indicatorType)
class indicatorTypeAdmin(admin.ModelAdmin):
    search_fields = ('name', 'id')

@admin.register(Concodance)
class ConcodanceAdmin(admin.ModelAdmin):
    search_fields = ('county', 'period_start', 'period_end',
                     'indicator_name', 'percentage')
    list_filter = ['county', 'period_start', 'period_end', 'indicator_name', 'period_end',
                   'indicator_name', 'percentage', ]
    list_display = ['county', 'period_start', 'period_end',
                    'indicator_name', 'percentage', ]
