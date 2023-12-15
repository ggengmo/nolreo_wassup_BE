from rest_framework import serializers
from .models import (
    Lodging,
    LodgingImage,
    # RoomType,
    # Amenity,
    # SubLocation,
    # MainLocation,
)

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

    class Meta:
        model = Lodging
        fields = ['name', 'intro', 'notice', 'info', 'sub_location']
