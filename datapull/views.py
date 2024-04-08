from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework import status
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from .utils import PMTCTDataClient
from .models import *
from .serializers import *

class ScheduleView(APIView):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, pk):
        try:
            return schedule_settings.objects.get(pk=pk)
        except schedule_settings.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        recs = schedule_settings.objects.all()
        serializer = ScheduleSerializer(
            recs, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        schedule = self.get_object(pk)
        serializer = ScheduleSerializer(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        schedule = self.get_object(pk)
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MiddlewareSettingsViewSet(viewsets.ModelViewSet):
    queryset = middleware_settings.objects.all()
    serializer_class = middleware_settingSerializer
    permission_classes = ()

@api_view()
def sync_data(request):
    sets = middleware_settings.objects.all().first()
    return Response({"id": sets.id, "synctdata": str(sets.syncdata).lower(), "client_url": sets.client_url})

class DataClientViewSet(viewsets.ViewSet):
    authentication_classes = [BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        ou:org_level & org_id
        pe:period i.e 202309(sept 2023)
        """
        params = request.data.get('params',{
            'dimension': ['pe:202309', 'ou:LEVEL-5;fVra3Pwta0Q'],
            'outputIdScheme': 'NAME'
        })
        credentials = ('healthit', 'rr23H3@1th1Tmtct')
        url = "https://khis.pmtct.uonbi.ac.ke/api/29/analytics.json"
        client = PMTCTDataClient(url,params=params, credentials=credentials)
        data = client.pull_data()
        return Response(data)
