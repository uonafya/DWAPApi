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


class IndicatorGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = indicatorGroups
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['username'])

        user.set_password(validated_data['password'])
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        token = Token.objects.create(user=user)
        return token.user


class middleware_settingSerializer(serializers.ModelSerializer):
    class Meta:
        model = middleware_settings
        fields = '__all__'


class ComparisonDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = final_comparison_data
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = indicator_category
        fields = '__all__'


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = counties
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = schedule_settings
        fields = '__all__'


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data_Mapping_Files
        fields = '__all__'


class mappedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = mapped_data
        fields = '__all__'
