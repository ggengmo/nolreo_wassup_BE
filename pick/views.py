from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db import IntegrityError

from .models import Pick
from .serializers import LodgingPickSerializer
from utils.permissions import CustomJWTAuthentication, CustomIsAuthenticated, IsOwner

class LodgingPickViewSet(ModelViewSet):
    serializer_class = LodgingPickSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [CustomIsAuthenticated, IsOwner]
    queryset = Pick.objects.all()

    def get_queryset(self):
        '''
        유저가 찜한 숙소 목록 조회 API
        '''
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
    
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
