from django.urls import path, include
from .views import BusViewSet, TrainViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('bus', BusViewSet)
router.register('train', TrainViewSet)

urlpatterns = [
    path('', include(router.urls)),
]