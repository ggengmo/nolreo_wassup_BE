from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.LodgingViewSet)
router.register('images', views.LodgingImageViewSet, basename='lodging_image')

urlpatterns = [
    path('', include(router.urls)),
]
