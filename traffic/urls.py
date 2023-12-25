from django.urls import path, include
from .views import (BusViewSet, TrainViewSet, 
                    RentalCarViewSet, RentalCarImageViewSet,
                    RentalCarReviewViewSet, RentalCarReviewCommentViewSet,
                    RentalCarReviewImageViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('bus', BusViewSet)
router.register('train', TrainViewSet)
router.register('rentalcar', RentalCarViewSet)
router.register('review', RentalCarReviewViewSet)
router.register(r'review/(?P<review_pk>\d+)/reply', RentalCarReviewCommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('rentalcar/image/<int:image_pk>/', RentalCarImageViewSet.as_view({'delete': 'destroy'})),
    path('review/image/<int:image_pk>/', RentalCarReviewImageViewSet.as_view({'delete': 'destroy'})),
]