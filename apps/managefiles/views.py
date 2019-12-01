from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from apps.managefiles.serializers import UploadSerializer
from apps.managefiles.models import Upload

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins, permissions, authentication
import urllib
from rest_framework.permissions import IsAuthenticated
from apps.utils.permissions import IsOwnerOrReadOnly


class UploadViewSet(viewsets.ModelViewSet):
    serializer_class = UploadSerializer
    queryset = Upload.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def create(self, request, *args, **kwargs):
        file = request.data.dict()
        file['file'] = request.FILES.get('files')
        serial = UploadSerializer(data=file)
        if not serial.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serial.save()
        host = 'http://' + request.META['HTTP_HOST']
        return Response({'host':host,'file':serial.data['file']})

    def list(self, request, *args, **kwargs):
        self.serializer_class = UploadSerializer
        self.queryset = Upload.objects.all()
        return super(UploadViewSet, self).list(request)


class UploadShopViewSet(viewsets.ModelViewSet):
    serializer_class = UploadSerializer
    queryset = Upload.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def create(self, request, *args, **kwargs):
        file = request.data.dict()
        if request.FILES.get('cover'):
            file['cover'] = request.FILES.get('cover')
        if request.FILES.get('big'):
            file['big'] = request.FILES.get('big')

        serial = UploadSerializer(data=file)
        if not serial.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serial.save()
        host = 'http://' + request.META['HTTP_HOST']
        files = {'big':serial.data['big'],'cover':serial.data['cover']}
        return Response({'host':host,'info':files})