from django.urls import path, include
from .views import BusViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('bus', BusViewSet)

urlpatterns = [
    path('', include(router.urls)),
]