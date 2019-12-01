from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from apps.managefiles.models import Upload


class UploadSerializer(ModelSerializer):
    class Meta:
        model = Upload
        fields = '__all__'