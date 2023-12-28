from django.db import models

class MainLocation(models.Model):
    '''
    메인 지역 모델
    '''
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.address
    

class SubLocation(models.Model):
    '''
    서브 지역 모델
    '''
    address = models.CharField(max_length=100)
    main_location = models.ForeignKey('MainLocation', on_delete=models.CASCADE, related_name='sub_locations')

    def __str__(self):
        return f'{self.main_location} {self.address}'
    

class Lodging(models.Model):
    '''
    숙소 모델
    '''
    name = models.CharField(max_length=100)
    intro = models.TextField()
    notice = models.TextField()
    info = models.TextField()
    sub_location = models.ForeignKey('SubLocation', on_delete=models.CASCADE, related_name='lodgings')
    
    def __str__(self):
        return self.name
    

class RoomType(models.Model):
    '''
    객실 타입 모델
    '''
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    price = models.IntegerField()
    lodging = models.ForeignKey('Lodging', on_delete=models.CASCADE, related_name='room_types')

    def __str__(self):
        return self.name
    

class RoomImage(models.Model):
    '''
    객실 이미지 모델
    '''
    image = models.ImageField(upload_to='room_images/%Y/%m/%d/', null=True, blank=True)
    is_main = models.BooleanField(default=False)
    room_type = models.ForeignKey('RoomType', on_delete=models.CASCADE, related_name='room_images')

    def __str__(self):
        return self.image.url


class Amenity(models.Model):
    '''
    편의시설 모델
    '''
    name = models.CharField(max_length=100)
    lodging = models.ForeignKey('Lodging', on_delete=models.CASCADE, related_name='amenities')

    def __str__(self):
        return self.name
    

class LodgingImage(models.Model):
    '''
    숙소 이미지 모델
    '''
    image = models.ImageField(upload_to='lodging_images/%Y/%m/%d/', null=True, blank=True)
    is_main = models.BooleanField(default=False)
    lodging = models.ForeignKey('Lodging', on_delete=models.CASCADE, related_name='lodging_images')

    def __str__(self):
        return self.image.url
    

class LodgingReview(models.Model):
    '''
    숙소 리뷰 모델
    '''
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
    star_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='lodging_reviews')
    lodging = models.ForeignKey('Lodging', on_delete=models.CASCADE, related_name='lodging_reviews')

    def __str__(self):
        return f'{self.title}:{self.content}'
    

class LodgingReviewImage(models.Model):
    '''
    숙소 리뷰 이미지 모델
    '''
    image = models.ImageField(upload_to='lodging_review_images/%Y/%m/%d/')
    lodging_review = models.ForeignKey('LodgingReview', on_delete=models.CASCADE, related_name='lodging_review_images')

    def __str__(self):
        return self.image.url
    

class LodgingReviewComment(models.Model):
    '''
    숙소 리뷰 댓글 모델
    '''
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='lodging_review_comments')
    lodging_review = models.ForeignKey('LodgingReview', on_delete=models.CASCADE, related_name='lodging_review_comments')

    def __str__(self):
        return self.content