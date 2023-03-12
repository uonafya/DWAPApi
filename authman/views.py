from http import client
from django.contrib.auth import authenticate
from .serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
from rest_framework import permissions, authentication
from .models import *
from django.contrib.auth import logout
from .serializers import *
from .models import *
import json
from json import JSONEncoder
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
import re
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import EmailMessage

from django.contrib.auth import get_user_model
User = get_user_model()


class RegistrationView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = UserSerializer


class EmailConfirmView(APIView):
    user = None
    checktoken = None

    def get(self, request, uidb64, token):
        try:
            id = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=id)
            checktoken = default_token_generator.make_token(user)
        except User.DoesNotExist:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        if user != None and token == checktoken:
            user.is_active = True
            user.save()

        return Response('Email confirmed!')


class LogOutView(APIView):
    permission_classes = ()

    def post(self, request,):
        logout(request.user)
        return Response({"Logout Success!"}, status=status.HTTP_200_OK)


class LoginView(APIView):

    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request,):
        # print(request.POST)
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        screens_set = set()
        if user:
            for role in user.groups.all():
                print(role)
                screens = [re.sub(' ', '', s['screens']) for s in RoleScreens.objects.filter(
                    role_id=role).values("screens")]
                for screen in screens:
                    screens_set.add(screen)
            print(screens_set)
            return Response({"user": {"username": user.username, "email": user.email, "id": user.id, "token": user.auth_token.key}, "roles": user.groups.values() if user.groups else None, "screens": list(screens_set)})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = (
    #     authentication.TokenAuthentication, authentication.BasicAuthentication)
