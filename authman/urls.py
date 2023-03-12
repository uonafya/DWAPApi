from rest_framework.routers import DefaultRouter
# from .apiviews import PollViewSet

from django.urls import path
from . views import *

router = DefaultRouter()
router.register('listusers', UserViewSet)

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="user_create"),
    path('register/confirm-email/<str:uidb64><str:token>/',
         EmailConfirmView.as_view(), name='email_confirm'),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogOutView.as_view(), name="logout"),
]
urlpatterns += router.urls
