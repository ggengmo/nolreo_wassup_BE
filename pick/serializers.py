from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Pick

class LodgingPickSerializer(ModelSerializer):
    '''
    숙소 찜 serializer
    '''
    class Meta:
        model = Pick
        fields = ['id', 'user', 'lodging', 'pick_type']
