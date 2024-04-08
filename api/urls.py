from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, register_converter
from .converters import DateConverter
from .generate_records import *
from .insights import *
register_converter(DateConverter, 'date')

router = DefaultRouter()
router.register('listfiles', FileUploadViewSet)
router.register('listindicators', IndicatorViewSet)
router.register('listindicator_types', IndicatorTypeViewSet)
router.register('listcounties', CountyViewSet)

urlpatterns = [
    path('create_indicator/', IndicatorCreate.as_view(), name='create_indicator'),
    path('create_indicator_type/',
         IndicatorTypeCreate.as_view(), name='create_indicator_type'),
    path('indicators/<int:limit>/', IndicatorList.as_view(),
         name='indicators'),
    path('indicators/filter/<date:from_date>/<date:to_date>/<int:limit>/', IndicatorFilter.as_view(),
         name='filter_ind'),
    path('indicatorscount/', get_count,
         name='indicators_count'),
    path('total_records_count/', get_records_count,
         name='total_records_count'),
    path('total_count/', total_count,
         name='total_count'),
    #     path('map_data/<str:county>/<str:category>/<date:from_date>/<date:to_date>/<int:limit>/', map_data,
    #          name='map_data'),
    path('generate_comparison_file/<str:data_source>/<str:county>/<str:category>/<date:from_date>/<date:to_date>/',
         generate_comparison_file, name='generate_comparison_file'),
    path('get_mapped_data', GetMappedFiles.as_view(),
         name='get_mapped_data'),
    path('get_comparison_data/<str:county>/<str:category>/<date:from_date>/<date:to_date>/', GetComparisonRecords.as_view(),
         name='get_comparison_data'),
    path('loadfacilities/', load_facilities,
         name='load_facilities'),

    ############################################ insights##################################
    path('insights/group_concodance/', CountyConcodance.as_view(),
         name='group_concodance'),
    path('insights/facilty_concodance/', FaciltyConcodance.as_view(),
         name='facilty_concodance'),
    path('insights/assets/', AssetsCount.as_view(),
         name='assets'),
]
urlpatterns += router.urls
