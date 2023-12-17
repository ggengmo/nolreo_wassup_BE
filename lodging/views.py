# Rest Framework
from rest_framework import viewsets, generics, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from utils.permissions import CustomJWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

# Models
from .models import (
    Lodging,
    LodgingImage,
    LodgingReview,
    LodgingReviewImage
    )
from .serializers import (
    LodgingSerializer,
    LodgingImageSerializer,
    LodgingReviewSerializer,
    LodgingReviewImageSerializer,
    )

class LodgingImageViewSet(viewsets.ModelViewSet):
    '''
    숙소 이미지 ViewSet
    '''
    queryset = LodgingImage.objects.all()
    serializer_class = LodgingImageSerializer
    action_map = {
        'put': 'partial_update',
    }

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
class LodgingViewSet(viewsets.ModelViewSet):
    '''
    숙소 ViewSet
    '''
    queryset = Lodging.objects.all()
    serializer_class = LodgingSerializer
    action_map = {
        'put': 'partial_update',
    }

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class LodgingReviewViewSet(viewsets.ModelViewSet):
    '''
    숙소 리뷰 ViewSet
    '''
    queryset = LodgingReview.objects.all()
    serializer_class = LodgingReviewSerializer
    authentication_classes = [CustomJWTAuthentication]
    action_map = {
        'put': 'partial_update',
    }

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class LodgingReviewImageViewSet(viewsets.ModelViewSet):
    '''
    숙소 리뷰 이미지 ViewSet
    '''
    queryset = LodgingReviewImage.objects.all()
    serializer_class = LodgingReviewImageSerializer
    authentication_classes = [CustomJWTAuthentication]
    action_map = {
        'put': 'partial_update',
    }

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({'message': '해당 리뷰 이미지를 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
