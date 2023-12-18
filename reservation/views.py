from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import MethodNotAllowed
from django.core.exceptions import ObjectDoesNotExist

from .models import Reservation
from .serializers import LodgingReservationSerializer
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
        obj = Reservation.objects.all().filter(user=self.request.user, room=self.kwargs['pk']).first()
        if not obj:
            raise ObjectDoesNotExist()
        return obj
    
    def partial_update(self, request, *args, **kwargs):
        try:
            return super().partial_update(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({'message': '해당 숙소를 예약한 기록이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({'message': '해당 숙소를 예약한 기록이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, instance):
        raise MethodNotAllowed('Detail GET', detail="Detail GET method is not allowed")