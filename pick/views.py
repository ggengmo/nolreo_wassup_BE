from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db import IntegrityError

from .serializers import LodgingPickSerializer
from utils.permissions import CustomJWTAuthentication, CustomIsAuthenticated, IsOwner

class LodgingPickViewSet(ModelViewSet):
    serializer_class = LodgingPickSerializer
    authentication_classes = [CustomJWTAuthentication]

    def get_permissions(self):
        permission_classes = [CustomIsAuthenticated]
        if self.action in ['list', 'partial_update']:
            permission_classes.append(IsOwner)
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        '''
        숙소 찜 생성 API
        '''
        try:
            data = super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({'message': '이미 찜한 숙소입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        return data


lodging_pick = LodgingPickViewSet.as_view({
    'post': 'create',
    'get': 'list',
    'patch': 'partial_update',
})
