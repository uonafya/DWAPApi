from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, register_converter
from .views import *


urlpatterns = [
    path('rules/cols/', SeriesColsView.as_view()),
    path('rules/cols/<int:pk>/',
         SeriesColsView.as_view()),

    path('rules/regex/', SeriesRegexView.as_view()),
    path('rules/regex/<int:pk>/',
         SeriesRegexView.as_view()),

    path('rules/rename/', RenameColsView.as_view()),
    path('rules/rename/<int:pk>/',
         RenameColsView.as_view()),

    path('rules/elements/', ComparisonElementsView.as_view()),
    path('rules/elements/<int:pk>/',
         ComparisonElementsView.as_view()),

    path('rules/misc/', MisSettingsView.as_view()),
    path('rules/misc/<int:pk>/',
         MisSettingsView.as_view()),

]
