from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions, authentication
from .models import *
from authman.models import *
from .serializers import *
from authman.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
from django.http import Http404


class IndicatorViewSet(viewsets.ModelViewSet):
    queryset = indicators.objects.all()
    serializer_class = IndicatorSerializer
    permission_classes = ()


class ScheduleView(APIView):
    serializer_class = RolesScreensSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, pk):
        try:
            return RoleScreens.objects.get(pk=pk)
        except RoleScreens.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        roles = RoleScreens.objects.all().values("role_id", "role_id__name", "screens")
        context = []
        for role in roles:
            print(role)
            context.append({'id': role["role_id"],
                            "role_name": role["role_id__name"], "screens": role["screens"]})
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


class RolesView(APIView):
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


class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = Data_Mapping_Files.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = ()

    # def create(self, request):
    #     try:
    #         serializer = FileUploadSerializer(
    #             data=request.data, context={"request": request})
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()

    #         dict_response = {"error": False,
    #                          "message": "File Saved Successfully"}
    #     except:
    #         dict_response = {"error": True,
    #                          "message": "Error During Saving Data"}
    #     return Response(dict_response)

    def list(self, request):
        files = Data_Mapping_Files.objects.all()
        serializer = FileUploadSerializer(
            files, many=True, context={"request": request})
        response_dict = {"error": False,
                         "message": "All  List Data", "data": serializer.data}
        return Response(response_dict)


class IndicatorCreate(generics.CreateAPIView):
    serializer_class = IndicatorSerializer
    permission_classes = [permissions.IsAuthenticated,]


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


class GetComparisonRecords(generics.ListAPIView):
    serializer_class = ComparisonDataSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        from_date = self.kwargs['from_date']
        to_date = self.kwargs['to_date']
        county = self.kwargs['county']
        category = self.kwargs['category']
        return final_comparison_data.objects.filter(Q(county__icontains=county, category__icontains=category), created__range=[from_date, to_date])


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


class IndicatorCatsViewSet(viewsets.ModelViewSet):
    queryset = indicator_category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = ()


class CountyViewSet(viewsets.ModelViewSet):
    queryset = counties.objects.all()
    serializer_class = CountySerializer
    permission_classes = ()


class IndicatorGroupCreate(generics.CreateAPIView):
    serializer_class = IndicatorGroupSerializer
    permission_classes = ()


class MiddlewareSettingsViewSet(viewsets.ModelViewSet):
    queryset = middleware_settings.objects.all()
    serializer_class = middleware_settingSerializer
    permission_classes = ()
