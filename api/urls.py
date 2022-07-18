from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *

router = DefaultRouter()
router.register('listusers', UserViewSet),
router.register('listindicators', IndicatorViewSet)
router.register('listindicator_types', IndicatorTypeViewSet)
router.register('listindicator_groups', IndicatorGroupViewSet)

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
    path('indicators/filter/<str:from>/<str:to>/', IndicatorList.as_view(),
         name='filter_ind'),
    path('indicatorscount/', get_count,
         name='indicators_count'),
]

urlpatterns += router.urls
