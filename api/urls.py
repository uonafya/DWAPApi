from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, register_converter
from .converters import DateConverter
from .data_mapping import *
register_converter(DateConverter, 'date')

router = DefaultRouter()
router.register('listusers', UserViewSet)
router.register('listschedules', ScheduleViewSet)
router.register('listfiles', FileUploadViewSet)
router.register('listindicators', IndicatorViewSet)
router.register('listindicator_types', IndicatorTypeViewSet)
router.register('listindicator_groups', IndicatorGroupViewSet)
router.register('listmiddleware_settings', MiddlewareSettingsViewSet)
router.register('listscounties', CountyViewSet)
router.register('listscategories', IndicatorCatsViewSet)

urlpatterns = [
    path("users/", UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
    path('create_indicator/', IndicatorCreate.as_view(), name='create_indicator'),
    path('create_indicator_type/',
         IndicatorTypeCreate.as_view(), name='create_indicator_type'),
    path('create_indicator_group/', IndicatorGroupCreate.as_view(),
         name='create_indicator_group'),
    path('indicators/<int:limit>/', IndicatorList.as_view(),
         name='indicators'),
    path('indicators/filter/<date:from_date>/<date:to_date>/<int:limit>/', IndicatorFilter.as_view(),
         name='filter_ind'),
    path('indicatorscount/', get_count,
         name='indicators_count'),
    path('total_records_count/', get_records_count,
         name='total_records_count'),
    path('sync_data/', sync_data,
         name='sync_data'),
    path('total_count/', total_count,
         name='total_count'),
    path('map_data/<str:category>/<date:from_date>/<date:to_date>/<int:limit>/', map_data,
         name='map_data'),
    path('generate_comparison_file/<str:use_api_data>/<str:county>/<str:category>/<date:from_date>/<date:to_date>/',
         generate_comparison_file, name='generate_comparison_file'),
    path('get_mapped_data', GetMappedFiles.as_view(),
         name='get_mapped_data'),
    path('get_comparison_data/<str:county>/<str:category>/<date:from_date>/<date:to_date>/', GetComparisonRecords.as_view(),
         name='get_comparison_data'),
    path('load_filter_data/', load_filter_data,
         name='load_filter_data'),
]
urlpatterns += router.urls
