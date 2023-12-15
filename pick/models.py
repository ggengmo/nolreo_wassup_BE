from django.db import models
from django.core.exceptions import ValidationError

class Pick(models.Model):
    '''
    사용자 찜 모델
    '''
    RESERVATION_TYPES = [
        ('LG', 'Lodging'),
        ('TR', 'Train'),
        ('BU', 'Bus'),
        ('RC', 'Rental Car'),
    ]
    lodging= models.ForeignKey('lodging.Lodging', on_delete=models.CASCADE, null=True, blank=True, related_name='lodging_pick')
    bus = models.ForeignKey('traffic.Bus', on_delete=models.CASCADE, null=True, blank=True, related_name='bus_pick')
    train = models.ForeignKey('traffic.Train', on_delete=models.CASCADE, null=True, blank=True, related_name='train_pick')
    rental_car = models.ForeignKey('traffic.RentalCar', on_delete=models.CASCADE, null=True, blank=True, related_name='rental_car_pick')
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='picks')
    pick_type = models.CharField(max_length=100, choices=RESERVATION_TYPES)

    def __str__(self):
        return f'{self.type}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'lodging'], name='unique_lodging_per_user'),
            models.UniqueConstraint(fields=['user', 'bus'], name='unique_bus_per_user'),
            models.UniqueConstraint(fields=['user', 'train'], name='unique_train_per_user'),
            models.UniqueConstraint(fields=['user', 'rental_car'], name='unique_rental_car_per_user'),
        ]

    def clean(self):
        # 이미 찜한 데이터인지 확인
        if Pick.objects.filter(user=self.user, lodging=self.lodging).exists():
            raise ValidationError("이미 찜한 숙소입니다.")
        if Pick.objects.filter(user=self.user, bus=self.bus).exists():
            raise ValidationError("이미 찜한 버스입니다.")
        if Pick.objects.filter(user=self.user, train=self.train).exists():
            raise ValidationError("이미 찜한 기차입니다.")
        if Pick.objects.filter(user=self.user, rental_car=self.rental_car).exists():
            raise ValidationError("이미 찜한 렌트카입니다.")