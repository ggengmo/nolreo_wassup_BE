from rest_framework import serializers
from django.db.models import Avg

from .models import (
    Lodging,
    LodgingImage,
    LodgingReview,
    LodgingReviewImage,
    LodgingReviewComment,
    RoomType,
    RoomImage,
    Amenity,
    MainLocation,
    SubLocation,
)

class MainLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainLocation
        fields = ['address']

    def validate(self, data):
        if data['address'] == '':
            raise serializers.ValidationError('주소를 입력해주세요.')
        return data
    

class SubLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubLocation
        fields = ['address', 'main_location']

    def validate(self, data):
        if data['address'] == '':
            raise serializers.ValidationError('상세주소를 입력해주세요.')
        return data


class LodgingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LodgingImage
        fields = ['image', 'is_main', 'lodging']


    def validate(self, data):
        if data['is_main']:
            lodging = data['lodging']
            if LodgingImage.objects.filter(lodging=lodging, is_main=True).exists():
                raise serializers.ValidationError('메인 이미지는 하나만 등록 가능합니다.')
        if data['image'] == None:
            raise serializers.ValidationError('숙소 이미지를 업로드해주세요.')
        return data
    

class LodgingSerializer(serializers.ModelSerializer):
    lodging_image = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    star_avg = serializers.SerializerMethodField()
    review_cnt = serializers.SerializerMethodField()

    class Meta:
        model = Lodging
        fields = ['name', 'intro', 'notice', 'info', 'sub_location', 'lodging_image', 'address', 'star_avg', 'review_cnt']


    def get_lodging_image(self, obj):
        try:
            lodging_image = obj.lodging_images.get(is_main=True)
        except:
            return None
        return LodgingImageSerializer(lodging_image).data
    
    def get_address(self, obj):
        return str(obj.sub_location)
    
    def get_star_avg(self, obj):
        return obj.lodging_reviews.aggregate(star_avg=Avg('star_score'))['star_avg']
    
    def get_review_cnt(self, obj):
        return obj.lodging_reviews.count()


class RoomTypeSerializer(serializers.ModelSerializer):
    room_image = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    lodging_name = serializers.SerializerMethodField()
    class Meta:
        model = RoomType
        fields = ['name', 'price', 'capacity', 'lodging', 'room_image', 'address', 'lodging_name']


    def validate(self, data):
        if data['name'] == '':
            raise serializers.ValidationError('방 종류를 입력해주세요.')
        if data['price'] <= 0:
            raise serializers.ValidationError('가격을 입력해주세요.')
        if data['capacity'] <= 0:
            raise serializers.ValidationError('수용 인원을 입력해주세요.')
        return data
    
    def get_room_image(self, obj):
        '''
        방 이미지를 같이 반환하기 위한 메소드
        '''
        try:
            room_image = obj.room_images.get(is_main=True)
        except:
            return None
        return RoomImageSerializer(room_image).data
    
    def get_address(self, obj):
        '''
        객실의 숙소 주소를 같이 반환하기 위한 메소드
        '''
        return str(obj.lodging.sub_location)
    
    def get_lodging_name(self, obj):
        '''
        객실의 숙소 이름을 같이 반환하기 위한 메소드
        '''
        return str(obj.lodging.name)

class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['image', 'is_main', 'room_type']


    def validate(self, data):
        if data['is_main']:
            room_type = data['room_type']
            if RoomImage.objects.filter(room_type=room_type, is_main=True).exists():
                raise serializers.ValidationError('메인 이미지는 하나만 등록 가능합니다.')
        return data


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['name', 'lodging']


    def validate(self, data):
        if data['name'] == '':
            raise serializers.ValidationError('편의시설을 입력해주세요.')
        return data


class LodgingReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LodgingReview
        fields = ['title', 'content', 'star_score', 'lodging', 'user']


    star_score = serializers.IntegerField(min_value=1, max_value=5)

    def validate(self, data):
        if data['title'] == '':
            raise serializers.ValidationError('제목을 입력해주세요.')
        if data['content'] == '':
            raise serializers.ValidationError('내용을 입력해주세요.')
        if data['star_score'] <= 0:
            raise serializers.ValidationError('별점을 입력해주세요.')
        return data


class LodgingReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LodgingReviewImage
        fields = ['image', 'lodging_review']


    def validate(self, data):
        if data['image'] == None:
            raise serializers.ValidationError('숙소 리뷰 이미지를 업로드해주세요.')
        return data


class LodgingReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LodgingReviewComment
        fields = ['content', 'lodging_review', 'user']


    def validate(self, data):
        if data['content'] == '':
            raise serializers.ValidationError('내용을 입력해주세요.')
        return data
    