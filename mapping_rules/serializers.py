from .models import *
from rest_framework import serializers


class SeriesColumnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeriesColumns
        fields = '__all__'


class KeyComparisonElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyComparisonElements
        fields = '__all__'


class SeriesRegexSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeriesRegex
        fields = '__all__'


class DatasetColumns_RanamingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetColumns_Ranaming
        fields = '__all__'


class MiscSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiscSettings
        fields = '__all__'
