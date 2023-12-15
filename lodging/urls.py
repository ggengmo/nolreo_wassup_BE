from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

images_router = DefaultRouter()
images_router.register('images', views.LodgingImageViewSet, basename='lodging_image')

images_router = DefaultRouter()
images_router.register('', views.LodgingImageViewSet, basename='lodging_image')

review_router = DefaultRouter()
review_router.register('', views.LodgingReviewViewSet, basename='lodging_review')

lodging_router = DefaultRouter()
lodging_router.register('', views.LodgingViewSet)

urlpatterns = [
    path('images/', include(images_router.urls)),
    path('review/', include(review_router.urls)),
    path('', include(lodging_router.urls)),
]