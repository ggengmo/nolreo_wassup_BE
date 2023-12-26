from datetime import datetime
from django.db.models import Avg
from rest_framework import serializers

from .models import Bus, Train, RentalCar, RentalCarImage, RentalCarReview, RentalCarReviewComment, RentalCarReviewImage

class BusSerializer(serializers.ModelSerializer):
    '''
    버스 생성 serializer
    '''
    rest_seat = serializers.SerializerMethodField()
    price_form = serializers.SerializerMethodField()
    class Meta:
        model = Bus
        fields = ['id', 'depart_point', 'dest_point', 'depart_time', 
                'arrival_time', 'num', 'price', 'rest_seat', 'price_form']
    
    def validate(self, data):
        '''
        버스 유효성 검사 메서드
        '''
        if data['depart_point'] == data['dest_point']:
            raise serializers.ValidationError("출발지와 도착지가 같습니다. 출발지를 다시 설정해 주세요.")
        
        if data['depart_time'] >= data['arrival_time']:
            raise serializers.ValidationError("출발시간이 도착시간보다 같거나 늦습니다. 출발시간을 다시 설정해 주세요.")
        
        if data['depart_time'] <= datetime.now():
            raise serializers.ValidationError("출발시간이 현재시간보다 같거나 빠릅니다. 출발시간을 다시 설정해 주세요.")

        if data['arrival_time'] <= datetime.now():
            raise serializers.ValidationError("도착시간이 현재시간보다 같거나 빠릅니다. 도착시간을 다시 설정해 주세요.")
        return data
    
    def get_rest_seat(self, obj):
        '''
        버스 남은 좌석을 serializer에 포함시키는 메서드
        '''
        return 40 - obj.reservations.count()
    
    def get_price_form(self, obj):
        try:
            price_form = format(obj.price, ',')
            return price_form
        except:
            return None

class TrainSerializer(serializers.ModelSerializer):
    '''
    기차 생성 serializer
    '''
    rest_seat = serializers.SerializerMethodField()
    price_form = serializers.SerializerMethodField()
    class Meta:
        model = Train
        fields = ['id', 'depart_point', 'dest_point', 'depart_time', 
                'arrival_time', 'num', 'price', 'rest_seat', 'price_form']
        
    def validate(self, data):
        '''
        기차 유효성 검사 메서드
        '''
        if data['depart_point'] == data['dest_point']:
            raise serializers.ValidationError("출발지와 도착지가 같습니다. 출발지를 다시 설정해 주세요.")
        
        if data['depart_time'] >= data['arrival_time']:
            raise serializers.ValidationError("출발시간이 도착시간보다 같거나 늦습니다. 출발시간을 다시 설정해 주세요.")
        
        if data['depart_time'] <= datetime.now():
            raise serializers.ValidationError("출발시간이 현재시간보다 같거나 빠릅니다. 출발시간을 다시 설정해 주세요.")

        if data['arrival_time'] <= datetime.now():
            raise serializers.ValidationError("도착시간이 현재시간보다 같거나 빠릅니다. 도착시간을 다시 설정해 주세요.")
        return data
    
    def get_rest_seat(self, obj):
        '''
        기차 남은 좌석을 serializer에 포함시키는 메서드
        '''
        return 400 - obj.reservations.count()
    
    def get_price_form(self, obj):
        try:
            price_form = format(obj.price, ',')
            return price_form
        except:
            return None
    

class RentalCarImageSerializer(serializers.ModelSerializer):
    '''
    렌트카 이미지 생성 serializer
    '''
    class Meta:
        model = RentalCarImage
        fields = ['image']

    def validate(self, data):
        '''
        렌트카 이미지 유효성 검사 메서드
        '''
        if data['image'] == '':
            raise serializers.ValidationError("이미지가 없습니다. 이미지를 입력해 주세요.")
        return data
    

class RentalCarSerializer(serializers.ModelSerializer):
    '''
    렌트카 생성 serializer
    '''
    car_image = serializers.SerializerMethodField()
    star_avg = serializers.SerializerMethodField()
    review_cnt = serializers.SerializerMethodField()
    class Meta:
        model = RentalCar
        fields = ['id', 'model', 'area', 'num', 'price', 'car_image', 'star_avg', 'review_cnt']

    def validate(self, data):
        '''
        렌트카 유효성 검사 메서드
        '''
        if data['price'] <= 0:
            raise serializers.ValidationError("차량 가격이 0원 이하입니다. 1원 이상의 가격을 입력해 주세요.")
        if data['model'] == '':
            raise serializers.ValidationError("모델이 없습니다. 모델을 입력해 주세요.")
        if data['area'] == '':
            raise serializers.ValidationError("지역이 없습니다. 지역을 입력해 주세요.")
        if data['num'] == '':
            raise serializers.ValidationError("차량 번호가 없습니다. 차량 번호를 입력해 주세요.")
        return data
    
    def get_car_image(self, obj):
        '''
        렌트카 이미지를 serializer에 포함시키는 메서드
        '''
        try:
            image = obj.rental_car_images.all()[0]
        except:
            return None
        return RentalCarImageSerializer(image).data
    
    def get_star_avg(self, obj):
        return obj.rental_car_reviews.aggregate(star_avg=Avg('star_score'))['star_avg']
    
    def get_review_cnt(self, obj):
        return obj.rental_car_reviews.count()
    

class RentalCarReviewSerializer(serializers.ModelSerializer):
    '''
    렌트카 리뷰 생성 serializer
    '''
    class Meta:
        model = RentalCarReview
        fields = ['title', 'content', 'star_score', 'rental_car', 'user']

    def validate(self, data):
        '''
        렌트카 리뷰 유효성 검사 메서드
        '''
        if data['title'] == '':
            raise serializers.ValidationError("제목이 없습니다. 제목을 입력해 주세요.")
        if data['content'] == '':
            raise serializers.ValidationError("내용이 없습니다. 내용을 입력해 주세요.")
        if data['star_score'] <= 0:
            raise serializers.ValidationError("점수가 0점 이하입니다. 1점 이상의 점수를 입력해 주세요.")
        return data


class RentalCarReviewImageSerializer(serializers.ModelSerializer):
    '''
    렌트카 리뷰 이미지 생성 serializer
    '''
    class Meta:
        model = RentalCarReviewImage
        fields = ['image']

    def validate(self, data):
        '''
        렌트카 리뷰 이미지 유효성 검사 메서드
        '''
        if data['image'] == '':
            raise serializers.ValidationError("이미지가 없습니다. 이미지를 입력해 주세요.")
        return data


class RentalCarReviewCommentSerializer(serializers.ModelSerializer):
    '''
    렌트카 리뷰 댓글 생성 serializer
    '''
    class Meta:
        model = RentalCarReviewComment
        fields = ['content', 'rental_car_review', 'user']

    def validate(self, data):
        '''
        렌트카 리뷰 댓글 유효성 검사 메서드
        '''
        if data['content'] == '':
            raise serializers.ValidationError("내용이 없습니다. 내용을 입력해 주세요.")
        if data['rental_car_review'] == '':
            raise serializers.ValidationError("리뷰가 없습니다. 리뷰를 입력해 주세요.")
        if data['user'] == '':
            raise serializers.ValidationError("로그인이 필요합니다. 로그인을 해주세요.")
        if data['rental_car_review'].rental_car not in RentalCar.objects.all():
            raise serializers.ValidationError("존재하지 않는 리뷰에는 댓글을 달 수 없습니다.")
        return data