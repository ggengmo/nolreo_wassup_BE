from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404

from .models import Bus, Train, RentalCar, RentalCarImage
from .serializers import (BusSerializer, TrainSerializer, 
                        RentalCarSerializer, RentalCarImageSerializer)


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