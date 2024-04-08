from .models import *
from rest_framework import serializers

class middleware_settingSerializer(serializers.ModelSerializer):
    class Meta:
        model = middleware_settings
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = schedule_settings
        fields = '__all__'
