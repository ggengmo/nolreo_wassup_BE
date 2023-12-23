from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from .models import Pick
from .serializers import (LodgingPickSerializer, BusPickSerializer, 
                        TrainPickSerializer, RentalcarSerializer,
                        PickSerializer)
from utils.permissions import CustomJWTAuthentication, CustomIsAuthenticated, IsOwner

class LodgingPickViewSet(ModelViewSet):
    '''
    숙소 찜 ViewSet
    '''
    serializer_class = LodgingPickSerializer
    authentication_classes = [CustomJWTAuthentication]
    queryset = Pick.objects.all().filter(pick_type='LG')

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [CustomIsAuthenticated]
        else:
            permission_classes = [CustomIsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        '''
        유저가 찜한 숙소 목록 조회 메서드
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

    def get_object(self):
        obj = Pick.objects.all().filter(user=self.request.user, lodging=self.kwargs['pk'])
        if not obj:
            raise ObjectDoesNotExist()
        return obj
    
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({'message': '해당 숙소를 찜한 기록이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
    
class BusPickViewSet(ModelViewSet):
    '''
    버스 찜 ViewSet
    '''
    serializer_class = BusPickSerializer
    authentication_classes = [CustomJWTAuthentication]
    queryset = Pick.objects.all().filter(pick_type='BU')

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [CustomIsAuthenticated]
        else:
            permission_classes = [CustomIsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        '''
        유저가 찜한 버스 목록 조회 메서드
        '''
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
    
    def create(self, request, *args, **kwargs):
        '''
        버스 찜 생성 API
        '''
        try:
            data = super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({'message': '이미 찜한 버스입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        return data
    
    def get_object(self):
        obj = Pick.objects.all().filter(user=self.request.user, bus=self.kwargs['pk'])
        if not obj:
            raise ObjectDoesNotExist()
        return obj
    
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({'message': '해당 버스를 찜한 기록이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        

class TrainPickViewSet(ModelViewSet):
    '''
    기차 찜 ViewSet
    '''
    serializer_class = TrainPickSerializer
    authentication_classes = [CustomJWTAuthentication]
    queryset = Pick.objects.all().filter(pick_type='TR')

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [CustomIsAuthenticated]
        else:
            permission_classes = [CustomIsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        '''
        유저가 찜한 기차 목록 조회 메서드
        '''
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
    
    def create(self, request, *args, **kwargs):
        '''
        기차 찜 생성 API
        '''
        try:
            data = super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({'message': '이미 찜한 기차입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        return data
    
    def get_object(self):
        obj = Pick.objects.all().filter(user=self.request.user, train=self.kwargs['pk'])
        if not obj:
            raise ObjectDoesNotExist()
        return obj
    
    def destroy(self, request, *args, **kwargs):
        '''
        기차 찜 삭제 API
        '''
        try:
            return super().destroy(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({'message': '해당 기차를 찜한 기록이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        

class RentalCarPickViewSet(ModelViewSet):
    '''
    렌트카 찜 ViewSet
    '''
    serializer_class = RentalcarSerializer
    authentication_classes = [CustomJWTAuthentication]
    queryset = Pick.objects.all().filter(pick_type='RC')

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [CustomIsAuthenticated]
        else:
            permission_classes = [CustomIsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        '''
        렌트카 찜 생성 API
        '''
        try:
            data = super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({'message': '이미 찜한 렌트카입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        return data
        
    def get_queryset(self):
        '''
        유저가 찜한 렌트카 목록 조회 메서드
        '''
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
    
    def get_object(self):
        '''
        요청한 pk에 해당하는 렌트카 찜 객체 반환 메서드
        '''
        obj = Pick.objects.all().filter(user=self.request.user, rental_car=self.kwargs['pk'])
        if not obj:
            raise ObjectDoesNotExist()
        return obj
    
    def destroy(self, request, *args, **kwargs):
        '''
        렌트카 찜 삭제 API
        '''
        try:
            return super().destroy(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({'message': '해당 렌트카를 찜한 기록이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        

class PickListView(ListAPIView):
    '''
    전체 찜 목록 View
    '''
    serializer_class = PickSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [CustomIsAuthenticated, IsOwner]
    queryset = Pick.objects.all().filter()

    def get_queryset(self):
        '''
        유저가 찜한 찜 목록 조회 메서드
        '''
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


lodging_pick = LodgingPickViewSet.as_view({
    'post': 'create',
    'get': 'list',
    'delete': 'destroy',
})

bus_pick = BusPickViewSet.as_view({
    'post': 'create',
    'get': 'list',
    'delete': 'destroy',
})

train_pick = TrainPickViewSet.as_view({
    'post': 'create',
    'get': 'list',
    'delete': 'destroy',
})

rental_car_pick = RentalCarPickViewSet.as_view({
    'post': 'create',
    'get': 'list',
    'delete': 'destroy',
})

pick_list = PickListView.as_view()