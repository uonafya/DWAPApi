from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import *


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = indicators
        fields = '__all__'

    def get(self):
        total = indicators.objects.all().count()
        return total


class IndicatorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = indicatorType
        fields = '__all__'

class ComparisonDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = final_comparison_data
        fields = '__all__'


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = counties
        fields = ('name',)

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data_Mapping_Files
        fields = '__all__'


class mappedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = mapped_data
        fields = '__all__'
