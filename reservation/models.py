from django.db import models

class Reservation(models.Model):
    '''
    예약 모델
    '''
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    reservation_type = models.CharField(max_length=100)
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='reservations')
    room = models.ForeignKey('lodging.RoomType', on_delete=models.CASCADE, null=True, blank=True, related_name='reservations')
    bus = models.ForeignKey('traffic.Bus', on_delete=models.CASCADE, null=True, blank=True, related_name='reservations')
    train = models.ForeignKey('traffic.Train', on_delete=models.CASCADE, null=True, blank=True, related_name='reservations')
    rental_car = models.ForeignKey('traffic.RentalCar', on_delete=models.CASCADE, null=True, blank=True, related_name='reservations')

    def __str__(self):
        return f'이름: {self.user}, 예약일: {self.start_at}, 예약종료일: {self.end_at}'
