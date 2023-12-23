from django.contrib import admin
from .models import Lodging, LodgingImage, MainLocation, SubLocation, Amenity, LodgingReview, RoomType, RoomImage, LodgingReviewImage, LodgingReviewComment

admin.site.register(Lodging)
admin.site.register(LodgingImage)
admin.site.register(MainLocation)
admin.site.register(SubLocation)
admin.site.register(Amenity)
admin.site.register(LodgingReview)
admin.site.register(RoomType)
admin.site.register(RoomImage)
admin.site.register(LodgingReviewImage)
admin.site.register(LodgingReviewComment)