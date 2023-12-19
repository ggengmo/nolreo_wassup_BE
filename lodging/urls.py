from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'review/(?P<review_pk>\d+)/comment', views.LodgingReviewCommentViewSet)
router.register('review/image', views.LodgingReviewImageViewSet)
router.register('roomtype/image', views.RoomImageViewSet)
router.register('roomtype', views.RoomTypeViewSet)
router.register('review', views.LodgingReviewViewSet)
router.register('amenity', views.AmenityViewSet)
router.register('images', views.LodgingImageViewSet)
router.register('sublocation', views.SubLocationViewSet)
router.register('mainlocation', views.MainLocationViewSet)
router.register('', views.LodgingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]