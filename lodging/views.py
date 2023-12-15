# Rest Framework
from rest_framework import viewsets, generics, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

# Models
from .models import (
    Lodging,
    LodgingImage,
    LodgingReview,
    )
from .serializers import (
    LodgingSerializer,
    LodgingImageSerializer,
    LodgingReviewSerializer,
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
        '''
        숙소 리뷰 생성 API
        '''

        return super().create(request, *args, **kwargs)

lodging_review = LodgingReviewViewSet.as_view({
    'post': 'create',
    'get': 'list',
    'patch': 'partial_update',
})