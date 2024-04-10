from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'pmtct-data', DataClientViewSet, basename='pmtct-data')
router.register(r'eid-data', EIDVLDataViewSet, basename='eid-data')
router.register('listmiddleware_settings', MiddlewareSettingsViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('listschedules/', ScheduleView.as_view(), name='schedules'),
    path('listschedules/<int:pk>/',
         ScheduleView.as_view(), name='update_schedules'),
    path('sync_data/', sync_data,
         name='sync_data'),
]
