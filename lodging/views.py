# Rest Framework
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response

# Models
from .models import (
    Lodging,
    )
from .serializers import (
    LodgingSerializer,
    )

class LodgingViewSet(viewsets.ModelViewSet):
    '''
    숙소 ViewSet
    '''
    queryset = Lodging.objects.all()
    serializer_class = LodgingSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
