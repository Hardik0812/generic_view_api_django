from dataclasses import fields
from rest_framework import serializers
from api_app_1.models import Students


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Students
        fields  = '__all__'