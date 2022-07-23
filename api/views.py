from msilib.schema import ReserveCost
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions, authentication
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json


class UserCreate(generics.CreateAPIView):
    # authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):

    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = ()
    # permission_classes = []  # permissions.IsAuthenticated
    # authentication_classes = (authentication.TokenAuthentication)


class IndicatorViewSet(viewsets.ModelViewSet):
    queryset = indicators.objects.all()
    serializer_class = IndicatorSerializer
    permission_classes = ()


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = schedule_settings.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = ()


class IndicatorCreate(generics.CreateAPIView):
    serializer_class = IndicatorSerializer
    permission_classes = ()


class IndicatorTypeViewSet(viewsets.ModelViewSet):
    queryset = indicatorType.objects.all()
    serializer_class = IndicatorTypeSerializer
    permission_classes = ()


class IndicatorList(generics.ListAPIView):
    serializer_class = IndicatorSerializer
    permission_classes = ()

    def get_queryset(self):
        """
        Filter
        """
        limit = int(self.kwargs['limit'])
        return indicators.objects.all()[:limit]


class IndicatorFilter(generics.ListAPIView):
    serializer_class = IndicatorSerializer
    permission_classes = ()

    def get_queryset(self):
        limit = int(self.kwargs['limit'])
        from_date = self.kwargs['from_date']
        to_date = self.kwargs['to_date']
        return indicators.objects.filter(created__range=[from_date, to_date])[:limit]


@api_view()
def get_count(request):
    return Response({"total": indicators.objects.all().count()})


@api_view()
def get_records_count(request):
    try:
        records = total_records.objects.all()
        totalrecords = 0
        if len(records) <= 0:
            totalrecords = 0
        else:
            totalrecords = records[0].records
        print(totalrecords)
        return Response({"totalrecords": totalrecords})
    except Exception as e:
        print(e)
        return Response({"Error": e})


@api_view()
def sync_data(request):
    sets = middleware_settings.objects.all().first()
    return Response({"id": sets.id, "synctdata": str(sets.syncdata).lower(), "client_url": sets.client_url})


@csrf_exempt
def total_count(request):
    try:
        data = request.body.decode('utf-8')
        records = json.loads(data)
        print(records)
        myrecords = total_records.objects.all()
        if len(myrecords) > 0:
            myrecords = myrecords[0]
            myrecords.records = int(records['records'])
        else:
            myrecords = total_records(records=int(records['records']))
        myrecords.save()
        print(myrecords)
    except Exception as e:
        print(e)


class IndicatorTypeCreate(generics.CreateAPIView):
    serializer_class = IndicatorTypeSerializer
    permission_classes = ()


class IndicatorGroupViewSet(viewsets.ModelViewSet):
    queryset = indicatorGroups.objects.all()
    serializer_class = IndicatorGroupSerializer
    permission_classes = ()


class IndicatorGroupCreate(generics.CreateAPIView):
    serializer_class = IndicatorGroupSerializer
    permission_classes = ()


class MiddlewareSettingsViewSet(viewsets.ModelViewSet):
    queryset = middleware_settings.objects.all()
    serializer_class = middleware_settingSerializer
    permission_classes = ()
