from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

lodging_router = DefaultRouter()
lodging_router.register(r'', views.LodgingViewSet)

urlpatterns = [
    path('', include(lodging_router.urls)),
]
