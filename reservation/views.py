from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import MethodNotAllowed
from django.core.exceptions import ObjectDoesNotExist

from .models import Reservation
from .serializers import LodgingReservationSerializer, BusReservationSerializer
from utils.permissions import CustomJWTAuthentication, CustomIsAuthenticated, IsOwner

class LodgingReservationViewSet(ModelViewSet):
    '''
    숙소 예약 ViewSet
    '''
    serializer_class = LodgingReservationSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [CustomIsAuthenticated, IsOwner]
    queryset = Reservation.objects.all().filter(reservation_type='RO')
    action_map = {
        'patch': 'partial_update',
    }

    def get_queryset(self):
        '''
        유저가 예약한 숙소 목록 조회 메서드
        '''
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
    
    def get_object(self):
        '''
        유저가 예약한 숙소 조회 메서드
        '''
        obj = Reservation.objects.all().filter(
            user=self.request.user, room=self.kwargs['pk']).first()
        if not obj:
            raise ObjectDoesNotExist()
        return obj
    
    def partial_update(self, request, *args, **kwargs):
        '''
        숙소 예약 수정 메서드
        '''
        try:
            return super().partial_update(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({'message': '해당 숙소를 예약한 기록이 없습니다.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        '''
        숙소 예약 삭제 메서드
        '''
        try:
            return super().destroy(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({'message': '해당 숙소를 예약한 기록이 없습니다.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, instance):
        '''
        숙소 예약 조회 메서드
            - 해당 메서드는 사용하지 않음
        '''
        raise MethodNotAllowed('Detail GET', detail="Detail GET method is not allowed")
    

class BusReservationViewSet(ModelViewSet):
    '''
    버스 예약 ViewSet
    '''
    serializer_class = BusReservationSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [CustomIsAuthenticated, IsOwner]
    queryset = Reservation.objects.all().filter(reservation_type='BU')
    action_map = {
        'patch': 'partial_update',
    }

    def get_queryset(self):
        '''
        유저가 예약한 버스 목록 조회 메서드
        '''
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
    
    def get_object(self):
        '''
        유저가 예약한 버스 조회 메서드
        '''
        obj = Reservation.objects.all().filter(
            user=self.request.user, bus=self.kwargs['pk']).first()
        if not obj:
            raise ObjectDoesNotExist()
        return obj
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        '''
        버스 예약 수정 메서드
        '''
        try:
            return super().partial_update(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({'message': '해당 버스를 예약한 기록이 없습니다.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        '''
        버스 예약 삭제 메서드
        '''
        try:
            return super().destroy(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({'message': '해당 버스를 예약한 기록이 없습니다.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, instance):
        '''
        버스 예약 조회 메서드
            - 해당 메서드는 사용하지 않음
        '''
        raise MethodNotAllowed('Detail GET', detail="Detail GET method is not allowed")