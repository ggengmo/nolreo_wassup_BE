from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

review_comment_router = DefaultRouter()
review_comment_router.register('', views.LodgingReviewCommentViewSet, basename='lodging_review_comment')

review_image_router = DefaultRouter()
review_image_router.register('', views.LodgingReviewImageViewSet, basename='lodging_review_image')

images_router = DefaultRouter()
images_router.register('', views.LodgingImageViewSet, basename='lodging_image')

review_router = DefaultRouter()
review_router.register('', views.LodgingReviewViewSet, basename='lodging_review')

lodging_router = DefaultRouter()
lodging_router.register('', views.LodgingViewSet)

urlpatterns = [
    path('review/<int_pk>/comment/', include(review_comment_router.urls)),
    path('review/image/', include(review_image_router.urls)),
    path('images/', include(images_router.urls)),
    path('review/', include(review_router.urls)),
    path('', include(lodging_router.urls)),
]