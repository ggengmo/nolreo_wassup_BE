from rest_framework import serializers
from .models import (
    Lodging,
)

class LodgingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lodging
        fields = ['name', 'intro', 'notice', 'info', 'price', 'sub_location']
        # read_only_fields = ['id', 'created_at', 'updated_at']