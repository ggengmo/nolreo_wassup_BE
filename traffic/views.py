from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Bus, Train, RentalCar, RentalCarImage, RentalCarReview, RentalCarReviewComment, RentalCarReviewImage
from .serializers import (BusSerializer, TrainSerializer, 
                        RentalCarSerializer, RentalCarImageSerializer,
                        RentalCarReviewSerializer, RentalCarReviewCommentSerializer,
                        RentalCarReviewImageSerializer)
from utils.permissions import CustomJWTAuthentication, CustomIsAuthenticated, IsOwner


class BusViewSet(viewsets.ModelViewSet):
    '''
    버스 생성 API
    '''
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        '''
        쿼리 파라미터에 따라 버스 목록을 필터링하는 메서드
            예약 목록 중에서 출발일과 도착일이 맞는 경우만 필터링
        '''
        if self.action == 'list':
            queryset = super().get_queryset()
            depart_point = self.request.query_params.get('depart_point', None)
            dest_point = self.request.query_params.get('dest_point', None)
            depart_time = self.request.query_params.get('depart_time', None)
            arrival_time = self.request.query_params.get('arrival_time', None)
            if depart_point:
                queryset = queryset.filter(depart_point=depart_point)
            if dest_point:
                queryset = queryset.filter(dest_point=dest_point)
            if depart_time:
                depart_time
                queryset = queryset.filter(depart_time__range=[depart_time, arrival_time])
            if arrival_time:
                arrival_time
                queryset = queryset.filter(arrival_time__range=[depart_time, arrival_time])
        try:
            return queryset
        except:
            return super().get_queryset()
    

class TrainViewSet(viewsets.ModelViewSet):
    '''
    기차 생성 API
    '''
    queryset = Train.objects.all()
    serializer_class = TrainSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        '''
        쿼리 파라미터에 따라 버스 목록을 필터링하는 메서드
            예약 목록 중에서 출발일과 도착일이 맞는 경우만 필터링
        '''
        if self.action == 'list':
            queryset = super().get_queryset()
            depart_point = self.request.query_params.get('depart_point', None)
            dest_point = self.request.query_params.get('dest_point', None)
            depart_time = self.request.query_params.get('depart_time', None)
            arrival_time = self.request.query_params.get('arrival_time', None)
            if depart_point:
                queryset = queryset.filter(depart_point=depart_point)
            if dest_point:
                queryset = queryset.filter(dest_point=dest_point)
            if depart_time:
                depart_time
                queryset = queryset.filter(depart_time__range=[depart_time, arrival_time])
            if arrival_time:
                arrival_time
                queryset = queryset.filter(arrival_time__range=[depart_time, arrival_time])
        try:
            return queryset
        except:
            return super().get_queryset()

class RentalCarViewSet(viewsets.ModelViewSet):
    '''
    렌트카 생성 API
    '''
    queryset = RentalCar.objects.all()
    serializer_class = RentalCarSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = RentalCarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rental_car = serializer.save()
        images = request.FILES.getlist('image')
        for image in images:
            rental_car_image = {'image': image}
            image_serializer = RentalCarImageSerializer(data=rental_car_image)
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save(rental_car=rental_car)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        '''
        쿼리 파라미터에 따라 렌트카 목록을 필터링하는 메서드
            -차량의 예약 목록 중에서 시작일이 예약 시작일과 종료일 사이에 있는 경우는 제외
            -차량의 예약 목록 중에서 종료일이 예약 시작일과 종료일 사이에 있는 경우는 제외
            -차량의 예약 목록 중에서 예약 시작일과 종료일이 모두 예약 시작일과 종료일 사이에 있는 경우는 제외
        '''
        if self.action == 'list':
            queryset = super().get_queryset()
            start_date = self.request.query_params.get('start_at', None)
            end_date = self.request.query_params.get('end_at', None)
            if start_date and end_date:          
                queryset = super().get_queryset()  
                queryset = queryset.filter(
                ~Q(reservations__start_at__range=[start_date, end_date]) &
                ~Q(reservations__end_at__range=[start_date, end_date]) &
                ~Q(reservations__start_at__lte=start_date, reservations__end_at__gte=end_date)
                )
            return queryset
        return super().get_queryset()
    
class RentalCarImageViewSet(viewsets.ModelViewSet):
    '''
    렌트카 이미지 삭제 API
    '''
    queryset = RentalCarImage.objects.all()
    serializer_class = RentalCarImageSerializer
    http_method_names = ['delete']
    permission_classes = [IsAdminUser]
    
    def destroy(self, request, image_pk):
        rental_car_image = get_object_or_404(RentalCarImage, pk=image_pk)
        rental_car_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class RentalCarReviewViewSet(viewsets.ModelViewSet):
    '''
    렌트카 리뷰 생성 API
    '''
    queryset = RentalCarReview.objects.all()
    serializer_class = RentalCarReviewSerializer
    authentication_classes = [CustomJWTAuthentication]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'partial_update']:
            permission_classes = [CustomIsAuthenticated, IsOwner]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def create(self, request):
        serializer = RentalCarReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rental_car_review = serializer.save()
        images = request.FILES.getlist('image')
        for image in images:
            rental_car_review_image = {'image': image}
            image_serializer = RentalCarReviewImageSerializer(data=rental_car_review_image)
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save(rental_car_review=rental_car_review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        '''
        렌트카 아이디가 있으면 해당 렌트카 리뷰만 반환
        '''
        queryset = super().get_queryset()
        if self.action == 'list':
            rental_car_id = self.request.query_params.get('rental_car_id')
            if rental_car_id is not None:
                queryset = queryset.filter(rental_car__id=rental_car_id)
        return queryset


class RentalCarReviewCommentViewSet(viewsets.ModelViewSet):
    '''
    렌트카 리뷰 댓글 생성 API
    '''
    queryset = RentalCarReviewComment.objects.all()
    serializer_class = RentalCarReviewCommentSerializer
    authentication_classes = [CustomJWTAuthentication]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'partial_update']:
            permission_classes = [CustomIsAuthenticated, IsOwner]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    

class RentalCarReviewImageViewSet(viewsets.ModelViewSet):
    '''
    렌트카 리뷰 이미지 삭제 API
    '''
    queryset = RentalCarReviewImage.objects.all()
    serializer_class = RentalCarReviewImageSerializer
    http_method_names = ['delete']
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, image_pk):
        rental_car_review_image = get_object_or_404(RentalCarReviewImage, pk=image_pk)
        rental_car_review_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)