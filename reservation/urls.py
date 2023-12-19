from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

lodging_router = DefaultRouter()
lodging_router.register('', views.LodgingReservationViewSet, basename='lodging_reservation')

bus_router = DefaultRouter()
bus_router.register('', views.BusReservationViewSet, basename='bus_reservation')

urlpatterns = [
    path('lodging/', include(lodging_router.urls)),
    path('bus/', include(bus_router.urls)),
]