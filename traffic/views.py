from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import viewsets
from .serializers import BusSerializer, TrainSerializer
from .models import Bus, Train


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