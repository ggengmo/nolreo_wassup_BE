from rest_framework import serializers
from rest_framework.fields import empty
from .models import Bus, Train, RentalCar, RentalCarImage
from datetime import datetime

class BusSerializer(serializers.ModelSerializer):
    '''
    버스 생성 serializer
    '''
    class Meta:
        model = Bus
        fields = ['depart_point', 'dest_point', 'depart_time', 
                'arrival_time', 'num', 'price']
    
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
    

class TrainSerializer(serializers.ModelSerializer):
    '''
    기차 생성 serializer
    '''
    class Meta:
        model = Train
        fields = ['depart_point', 'dest_point', 'depart_time', 
                'arrival_time', 'num', 'price']
        
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
    class Meta:
        model = RentalCar
        fields = ['model', 'area', 'num', 'price']

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