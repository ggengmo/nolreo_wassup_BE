from datetime import datetime
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer

from .models import Reservation
from lodging.models import RoomType

class LodgingReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'room', 'reservation_type', 'start_at', 'end_at']


    def validate(self, data):
        '''
        숙소 예약 생성 시 유효성 검사
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
                raise serializers.ValidationError({"message":"이미 예약된 날짜입니다."})
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