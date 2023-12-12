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
    main_location = models.ForeignKey('MainLocation', on_delete=models.CASCADE)

    def __str__(self):
        return self.address
    

class Lodging(models.Model):
    '''
    숙소 모델
    '''
    name = models.CharField(max_length=100)
    intro = models.TextField()
    notice = models.TextField()
    info = models.TextField()
    sub_location = models.ForeignKey('SubLocation', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    

class RoomType(models.Model):
    '''
    객실 타입 모델
    '''
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    lodging = models.ForeignKey('Lodging', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class RoomImage(models.Model):
    '''
    객실 이미지 모델
    '''
    image = models.CharField(max_length=200)
    room_type = models.ForeignKey('RoomType', on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return self.image_url


class Amenity(models.Model):
    '''
    편의시설 모델
    '''
    name = models.CharField(max_length=100)
    lodging = models.ForeignKey('Lodging', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

