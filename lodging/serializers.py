from rest_framework import serializers
from .models import (
    Lodging,
)

class LodgingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lodging
        fields = ['name', 'intro', 'notice', 'info', 'sub_location']