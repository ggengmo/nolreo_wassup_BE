# Rest Framework
from rest_framework import viewsets, generics, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from utils.permissions import CustomJWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

# Models
from .models import (
    Lodging,
    LodgingImage,
    LodgingReview,
    LodgingReviewImage,
    LodgingReviewComment,
    )
from .serializers import (
    LodgingSerializer,
    LodgingImageSerializer,
    LodgingReviewSerializer,
    LodgingReviewImageSerializer,
    LodgingReviewCommentSerializer,
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
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
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
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
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
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    # # 해당 숙소를 예약한 사용자인지 확인 - 예약 기능 생성 후 추가예정
    # def create(self, request, *args, **kwargs):
    #     lodging_id = request.data['lodging']
    #     user = request.user
        
    #     if not Reservation.objects.filter(
    #         user=user, 
    #         lodging_id=lodging_id,
    #         end_at=timezone.now()).exists():
    #         raise PermissionDenied('해당 숙소에 대한 예약 이력이 없습니다.')
    #     return super().create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        try:
            review = self.get_object()
            if review.user != request.user:
                raise PermissionDenied('해당 리뷰의 작성자가 아닙니다.')
            return super().destroy(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({'message': '해당 리뷰를 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

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
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({'message': '해당 리뷰 이미지를 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        review_image = self.get_object()
        if review_image.lodging_review.user != request.user:
            raise PermissionDenied('해당 리뷰 이미지의 작성자가 아닙니다.')
        return super().partial_update(request, *args, **kwargs)
    
class LodgingReviewCommentViewSet(viewsets.ModelViewSet):
    '''
    숙소 리뷰 댓글 ViewSet
    '''
    queryset = LodgingReviewComment.objects.all()
    serializer_class = LodgingReviewCommentSerializer
    authentication_classes = [CustomJWTAuthentication]
    action_map = {
        'put': 'partial_update',
    }

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def destroy(self, request, *args, **kwargs):
        try:
            comment = self.get_object()
            if comment.user != request.user:
                raise PermissionDenied('해당 댓글의 작성자가 아닙니다.')
            return super().destroy(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({'message': '해당 댓글을 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            raise PermissionDenied('해당 댓글의 작성자가 아닙니다.')
        return super().partial_update(request, *args, **kwargs)
    