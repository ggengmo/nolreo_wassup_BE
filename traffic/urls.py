from django.urls import path, include
from .views import (BusViewSet, TrainViewSet, 
                    RentalCarViewSet, RentalCarImageViewSet,
                    RentalCarReviewViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('bus', BusViewSet)
router.register('train', TrainViewSet)
router.register('rentalcar', RentalCarViewSet)
router.register('review', RentalCarReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('rentalcar/image/<int:image_pk>/', RentalCarImageViewSet.as_view({'delete': 'destroy'})),
]