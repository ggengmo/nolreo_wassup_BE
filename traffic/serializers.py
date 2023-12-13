from rest_framework import serializers
from .models import Bus, Train
from datetime import datetime

class BusSerializer(serializers.ModelSerializer):
    '''
    버스 생성 serializer
    '''
    class Meta:
        model = Bus
        fields = ['depart_point', 'dest_point', 'depart_time', 
                'arrival_time', 'num']
    
    def validate(self, data):
        '''
        버스 유효성 검사 메서드
        '''
        if data['depart_point'] == data['dest_point']:
            raise serializers.ValidationError("출발지와 도착지가 같습니다.")
        
        if data['depart_time'] >= data['arrival_time']:
            raise serializers.ValidationError("출발시간이 도착시간보다 같거나 늦습니다.")
        
        if data['depart_time'] <= datetime.now():
            raise serializers.ValidationError("출발시간이 현재시간보다 같거나 빠릅니다.")

        if data['arrival_time'] <= datetime.now():
            raise serializers.ValidationError("도착시간이 현재시간보다 같거나 빠릅니다.")
        return data
    
    def create(self, validated_data):
        '''
        버스 생성 메서드
        '''
        bus = Bus.objects.create(**validated_data)
        return bus
    

class TrianSerializer(serializers.ModelSerializer):
    '''
    버스 생성 serializer
    '''
    class Meta:
        model = Train
        fields = ['depart_point', 'dest_point', 'depart_time', 
                'arrival_time', 'num']
    
    def validate(self, data):
        '''
        기차 유효성 검사 메서드
        '''
        if data['depart_point'] == data['dest_point']:
            raise serializers.ValidationError("출발지와 도착지가 같습니다.")
        
        if data['depart_time'] >= data['arrival_time']:
            raise serializers.ValidationError("출발시간이 도착시간보다 같거나 늦습니다.")
        
        if data['depart_time'] <= datetime.now():
            raise serializers.ValidationError("출발시간이 현재시간보다 같거나 빠릅니다.")

        if data['arrival_time'] <= datetime.now():
            raise serializers.ValidationError("도착시간이 현재시간보다 같거나 빠릅니다.")
        return data
    
    def create(self, validated_data):
        '''
        기차 생성 메서드
        '''
        bus = Bus.objects.create(**validated_data)
        return bus
