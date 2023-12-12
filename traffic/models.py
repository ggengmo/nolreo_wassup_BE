from django.db import models

class Train(models.Model):
    '''
    기차 모델
    '''
    depart_point = models.CharField(max_length=100)
    dest_point = models.CharField(max_length=100)
    depart_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    num = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.depart_point} 출발 {self.dest_point}행 {self.num}번 기차'
    

class Bus(models.Model):
    '''
    고속버스 모델
    '''
    depart_point = models.CharField(max_length=100)
    dest_point = models.CharField(max_length=100)
    depart_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    num = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.depart_point} 출발 {self.dest_point}행 {self.num}번 고속버스'
    

class RentalCar(models.Model):
    '''
    렌트카 모델
    '''
    model = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    num = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.model} 모델 {self.num}번 차량'
    

class RentalCarImage(models.Model):
    '''
    렌트카 이미지 모델
    '''
    image = models.ImageField(upload_to='rental_car/%Y/%m/%d/')
    rental_car = models.ForeignKey('RentalCar', on_delete=models.CASCADE, related_name='rental_car_images')
    
    def __str__(self):
        return f'{self.rental_car} 이미지'
    

class RentalCarReview(models.Model):
    '''
    렌트카 리뷰 모델
    '''
    title = models.CharField(max_length=100)
    content = models.TextField()
    star_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    rental_car = models.ForeignKey('RentalCar', on_delete=models.CASCADE, related_name='rental_car_reviews')
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='rental_car_reviews')
    
    def __str__(self):
        return f'{self.user}님의 {self.rental_car} 리뷰'
    

class RentalCarReviewImage(models.Model):
    '''
    렌트카 리뷰 이미지 모델
    '''
    image = models.ImageField(upload_to='rental_car_review/%Y/%m/%d/')
    rental_car_review = models.ForeignKey('RentalCarReview', on_delete=models.CASCADE, related_name='rental_car_review_images')
    
    def __str__(self):
        return f'{self.rental_car_review} 이미지'
    

class RentalCarReviewComment(models.Model):
    '''
    렌트카 리뷰 댓글 모델
    '''
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rental_car_review = models.ForeignKey('RentalCarReview', on_delete=models.CASCADE, related_name='rental_car_review_comments')
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='rental_car_review_comments')
    
    def __str__(self):
        return f'{self.user}님의 {self.rental_car_review} 댓글'