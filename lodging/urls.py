from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

images_router = DefaultRouter()
images_router.register('images', views.LodgingImageViewSet, basename='lodging_image')

review_router = DefaultRouter()
review_router.register('review', views.LodgingReviewViewSet, basename='lodging_review')

lodging_router = DefaultRouter()
lodging_router.register('', views.LodgingViewSet)

urlpatterns = [
    path('', include(images_router.urls)),
    path('', include(review_router.urls)),
    path('', include(lodging_router.urls)),
]
