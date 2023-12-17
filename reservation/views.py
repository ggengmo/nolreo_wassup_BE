from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import ValidationError

from .models import Reservation
from lodging.models import RoomType
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

    def get_queryset(self):
        '''
        유저가 예약한 숙소 목록 조회 메서드
        '''
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset