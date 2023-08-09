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
from rest_framework.authtoken.models import Token
from .models import *
from django.db.models import Subquery, OuterRef, Avg, Value
from django.db.models.functions import Concat
from django.contrib.auth import logout
from .models import *
from notifications.models import Notifications
import json
from json import JSONEncoder
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
import re
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import EmailMessage
from django.http import Http404
from django.utils import timezone
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
        # exists = False
        # if "admin" in str(username).lower():
        #     try:
        #         if User.objects.get(username=username):
        #             exists = True
        #     except Exception as e:
        #         exists = False
        #     newuser,created = User.objects.get_or_create(username=username, first_name="admin", last_name="admin",
        #                                          email="admin@admin.com", password=password, is_active=True, is_staff=True, is_superuser=True) if not exists else None
        # if exists:
        #     if not user.token:
        #         token,created=Token.objects.get_or_create(user=User.objects.get(
        #             username=username))
        user=User.objects.get(username=username)
        user = authenticate(username=username, password=password)
        # print(request.data)
        screens_set = set()
        facilities = set()
        counties = set()
        if user:
            notices = [
                {"created_by": notice.created_by.username, "notified_user": notice.notified_user.username, "message": notice.message, "date": notice.created_at} for notice in Notifications.objects.filter(notified_user=user, read=False)]
            for role in user.groups.all():
                rolemeta = RoleScreens.objects.get(role_id=role)
                for f in rolemeta.facilities.all():
                    facilities.add(f.name)
                for c in rolemeta.counties.all():
                    counties.add(c.name)
                screens = [str(s['screens']).strip() for s in RoleScreens.objects.filter(
                    role_id=role).values("screens")]
                for screen in screens:
                    screens_set.add(screen)
            # print(screens_set)
            return Response({
                "user": {"username": user.username, "email": user.email, "id": user.id, "token": user.auth_token.key},
                "roles": user.groups.values() if user.groups else None,
                "screens": list(screens_set),
                "facilities": list(facilities),
                "counties": list(counties),
                "notifications": notices})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class RolesScreensView(APIView):
    serializer_class = RolesScreensSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, pk):
        try:
            return RoleScreens.objects.get(pk=pk)
        except RoleScreens.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        roles = RoleScreens.objects.all()
        context = []
        facilities = set()
        counties = set()
        for role in roles:
            for f in role.facilities.all():
                facilities.add(f.name)
            for c in role.counties.all():
                counties.add(c.name)
            print(counties)
            context.append({'id': role.role_id.id,
                            "role_name": role.role_id.name, "screens": role.screens, "counties": list(counties), "facilities": list(facilities)})
        return Response(context)

    def post(self, request, format=None):
        serializer = RolesScreensSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        roles = self.get_object(pk)
        serializer = RolesScreensSerializer(roles, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        role = self.get_object(pk)
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        users = User.objects.all().values("username", "first_name", "last_name",
                                          "email", "phone", "groups__name", "organisation")
        context = list(users)
        return Response(context)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
