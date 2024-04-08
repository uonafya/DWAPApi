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

class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = Data_Mapping_Files.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = ()

    def create(self, request):
        try:
            # serializer = FileUploadSerializer(
            #     data=request.data, context={"request": request})
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
            files = request.FILES.getlist('mapping_file')
            print(files)
            if files:
                for f in files:
                    print(f.name)
                    p, created = Data_Mapping_Files.objects.get_or_create(
                        mapping_file=f)

            dict_response = {"icon": "success",
                             "message": "File Saved Successfully"}
        except:
            dict_response = {"icon": "error",
                             "message": "Error During Saving Data"}
        return Response(dict_response)

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
        return final_comparison_data.objects.filter(Q(county__icontains=county, category__icontains=category), create_date__range=[from_date, to_date])


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

class CountyViewSet(viewsets.ModelViewSet):
    queryset = counties.objects.all()
    serializer_class = CountySerializer
    permission_classes = ()

    def get_queryset(self):
        queryset = super().get_queryset()  # Get the initial queryset

        # Get the 'county' parameter from the request query parameters
        user = self.request.user
        if user != None:
            assigned_counties = RoleScreens.objects.filter(
                role_id__in=user.groups.all()).values("counties__name")
        if assigned_counties:
            # Apply the filter based on the 'county' parameter
            queryset = queryset.filter(name__in=assigned_counties)
        else:
            queryset = []
        return queryset

