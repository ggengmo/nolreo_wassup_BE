from datetime import datetime
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer

from traffic.models import Bus
from .models import Reservation
from lodging.models import RoomType

class LodgingReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'room', 'reservation_type', 'start_at', 'end_at']


    def validate(self, data):
        '''
        숙소 예약 생성&수정 시 유효성 검사
        1. 예약 시작일이 예약 종료일보다 늦은 경우
        2. 이미 예약된 날짜인지 확인
        3. 과거 날짜인지 확인
        '''
        # 예약 시작일이 예약 종료일보다 늦은 경우
        if data['start_at'] >= data['end_at']:
            raise serializers.ValidationError({"message":"예약 시작일이 예약 종료일보다 빨라야 합니다."})
        # 이미 예약된 날짜인지 확인
        reservations = Reservation.objects.filter(room=data['room'])
        for reservation in reservations:
            if (data['start_at'] <= reservation.end_at) and (data['end_at'] >= reservation.start_at):
                if self.context['request'].method == 'POST':
                    raise serializers.ValidationError({"message":"이미 예약된 날짜입니다."})
                elif self.context['request'].method == 'PATCH':
                    if self.instance.start_at != data['start_at'] and self.instance.end_at != data['end_at']:
                        raise serializers.ValidationError({"message":"이미 예약된 날짜입니다."})
                    else:
                        raise serializers.ValidationError(
                            {"message":"이전 예약 날짜와 같은 예약 날짜입니다."})
        # 과거 날짜인지 확인
        if data['start_at'] < datetime.today():
            raise serializers.ValidationError({"message":"과거 날짜는 선택할 수 없습니다."})
        return data
    
    def run_validation(self, data=...):
        '''
        숙소 예약 유효성 실행 메서드
            숙소 존재 여부 확인 에러 메시지 커스텀을 위한 오버라이딩
        '''
        if not RoomType.objects.filter(id=data['room']).exists():
            raise serializers.ValidationError({"message":"존재하지 않는 숙소입니다."})
        return super().run_validation(data)
    

class BusReservationSerializer(ModelSerializer):
    seat = serializers.IntegerField(min_value=1, max_value=40, write_only=True)
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'bus', 'reservation_type', 'start_at', 'end_at', 'seat']


    

    def validate(self, data):
        '''
        버스 예약 생성&수정 시 유효성 검사
            - 만석(40인) 여부 확인
            - 예약 대상 버스가 과거 버스인지 확인
        '''
        if self.context['request'].method == 'POST' or self.context['request'].method == 'PATCH':
            pre_passengers_cnt = Reservation.objects.filter(bus=data['bus']).count()
            passengers_cnt = pre_passengers_cnt + data['seat']
            if passengers_cnt > 40:
                raise serializers.ValidationError({"message":f"현재 탑승 가능 승객은 {40-pre_passengers_cnt}명으로 예약이 불가능합니다."})
        bus = Bus.objects.get(id=data['bus'].id)
        if bus.depart_time < datetime.today():
            raise serializers.ValidationError({"message":"과거 버스는 예약할 수 없습니다."})
        return data
    
    def create(self, validated_data):
        '''
        버스 예약 생성 메서드
        '''
        seat = validated_data.pop('seat')
        reservation = Reservation.objects.create(**validated_data)
        reservation.save()
        return reservation
    
    def run_validation(self, data=...):
        '''
        버스 예약 유효성 실행 메서드
            버스 존재 여부 확인 에러 메시지 커스텀을 위한 오버라이딩
        '''
        if not Bus.objects.filter(id=data['bus']).exists():
            raise serializers.ValidationError({"message":"존재하지 않는 버스입니다."})
        return super().run_validation(data)
