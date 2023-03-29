from rest_framework import permissions, authentication
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from django.http import Http404


class SeriesColsView(APIView):
    serializer_class = SeriesColumnsSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, pk):
        try:
            return SeriesColumns.objects.get(pk=pk)
        except SeriesColumns.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        recs = SeriesColumns.objects.all()
        serializer = SeriesColumnsSerializer(
            recs, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SeriesColumnsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        schedule = self.get_object(pk)
        serializer = SeriesColumnsSerializer(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        schedule = self.get_object(pk)
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SeriesRegexView(APIView):
    serializer_class = SeriesRegexSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, pk):
        try:
            return SeriesRegex.objects.get(pk=pk)
        except SeriesRegex.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        recs = SeriesRegex.objects.all()
        serializer = SeriesRegexSerializer(
            recs, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SeriesRegexSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        schedule = self.get_object(pk)
        serializer = SeriesRegexSerializer(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        schedule = self.get_object(pk)
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ComparisonElementsView(APIView):
    serializer_class = KeyComparisonElementsSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, pk):
        try:
            return KeyComparisonElements.objects.get(pk=pk)
        except KeyComparisonElements.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        recs = KeyComparisonElements.objects.all()
        serializer = KeyComparisonElementsSerializer(
            recs, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = KeyComparisonElementsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        schedule = self.get_object(pk)
        serializer = KeyComparisonElementsSerializer(
            schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        schedule = self.get_object(pk)
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MisSettingsView(APIView):
    serializer_class = MiscSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, pk):
        try:
            return MiscSettings.objects.get(pk=pk)
        except MiscSettings.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        recs = MiscSettings.objects.all()
        serializer = MiscSerializer(
            recs, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MiscSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        schedule = self.get_object(pk)
        serializer = MiscSerializer(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        schedule = self.get_object(pk)
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RenameColsView(APIView):
    serializer_class = DatasetColumns_RanamingSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, pk):
        try:
            return DatasetColumns_Ranaming.objects.get(pk=pk)
        except DatasetColumns_Ranaming.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        recs = DatasetColumns_Ranaming.objects.all()
        serializer = DatasetColumns_RanamingSerializer(
            recs, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DatasetColumns_RanamingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        schedule = self.get_object(pk)
        serializer = DatasetColumns_RanamingSerializer(
            schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        schedule = self.get_object(pk)
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
