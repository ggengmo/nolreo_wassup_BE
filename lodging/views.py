# Rest Framework
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from utils.permissions import CustomJWTAuthentication
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

# Custom
from .models import (
    Lodging,
    LodgingImage,
    LodgingReview,
    LodgingReviewImage,
    LodgingReviewComment,
    RoomType,
    RoomImage,
    Amenity,
    MainLocation,
    SubLocation,
    )
from .serializers import (
    LodgingSerializer,
    LodgingImageSerializer,
    LodgingReviewSerializer,
    LodgingReviewImageSerializer,
    LodgingReviewCommentSerializer,
    RoomTypeSerializer,
    RoomImageSerializer,
    AmenitySerializer,
    MainLocationSerializer,
    SubLocationSerializer,
    )
    
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

    def get_queryset(self):
        '''
        쿼리 파라미터에 따라 숙소 목록을 필터링하는 메서드
            객실의 숙소들의 예약 목록 중에서 시작일이 예약 시작일보다 작고 종료일이 예약 시작일보다 큰 경우는 제외
            객실의 숙소들의 예약 목록 중에서 시작일이 예약 시작일이랑 같은 경우 제외
            객실의 숙소들의 예약 목록 중에서 시작일이 예약 시작일보다 크고 시작일이 예약 종료일보다 작은 경우 제외
        '''
        if self.action == 'list':
            start_date = self.request.query_params.get('start_at', None)
            end_date = self.request.query_params.get('end_at', None)
            if start_date and end_date:
                queryset = super().get_queryset()
                queryset = queryset.filter(
                    # 객실의 숙소들의 예약 목록 중에서 시작일이 예약 시작일보다 작고 종료일이 예약 시작일보다 큰 경우는 제외
                    ~Q(room_types__reservations__start_at__lt=start_date, room_types__reservations__end_at__gt=start_date) &
                    # 객실의 숙소들의 예약 목록 중에서 시작일이 예약 시작일이랑 같은 경우 제외
                    ~Q(room_types__reservations__start_at=start_date) &
                    # 객실의 숙소들의 예약 목록 중에서 시작일이 예약 시작일보다 크고 시작일이 예약 종료일보다 작은 경우 제외
                    ~Q(room_types__reservations__start_at__gt=start_date, room_types__reservations__start_at__lt=end_date)
                )
                return queryset
        return super().get_queryset()
    
    
class MainLocationViewSet(viewsets.ModelViewSet):
    '''
    메인 지역 ViewSet
    '''
    queryset = MainLocation.objects.all()
    serializer_class = MainLocationSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
class SubLocationViewSet(viewsets.ModelViewSet):
    '''
    서브 지역 ViewSet
    '''
    queryset = SubLocation.objects.all()
    serializer_class = SubLocationSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class LodgingImageViewSet(viewsets.ModelViewSet):
    '''
    숙소 이미지 ViewSet
    '''
    queryset = LodgingImage.objects.all()
    serializer_class = LodgingImageSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        '''
        숙소 이미지 목록을 조회하는 경우 요청한 숙소에 해당하는 이미지만 반환
        '''
        if self.action == 'list':
            lodging_id = self.request.query_params.get('lodging_id', None)
            queryset = super().get_queryset()
            queryset = queryset.filter(lodging=lodging_id)
            return queryset
        return super().get_queryset()


class RoomTypeViewSet(viewsets.ModelViewSet):
    '''
    숙소 방 종류 ViewSet
    '''
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class RoomImageViewSet(viewsets.ModelViewSet):
    '''
    숙소 방 이미지 ViewSet
    '''
    queryset = RoomImage.objects.all()
    serializer_class = RoomImageSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    

class AmenityViewSet(viewsets.ModelViewSet):
    '''
    숙소 편의시설 ViewSet
    '''
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer

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

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    
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
