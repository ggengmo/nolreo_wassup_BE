from django.contrib import admin

from .models import Train, Bus, RentalCar, RentalCarImage, RentalCarReview, RentalCarReviewComment, RentalCarReviewImage

admin.site.register(Train)
admin.site.register(Bus)
admin.site.register(RentalCar)
admin.site.register(RentalCarImage)
admin.site.register(RentalCarReview)
admin.site.register(RentalCarReviewComment)
admin.site.register(RentalCarReviewImage)
