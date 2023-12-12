from django.db import models

class Pick(models.Model):
    '''
    사용자 찜 모델
    '''
    lodging= models.ForeignKey('lodging.Lodging', on_delete=models.CASCADE, null=True, blank=True, related_name='lodging_pick')
    bus = models.ForeignKey('traffic.Bus', on_delete=models.CASCADE, null=True, blank=True, related_name='bus_pick')
    train = models.ForeignKey('traffic.Train', on_delete=models.CASCADE, null=True, blank=True, related_name='train_pick')
    rental_car = models.ForeignKey('traffic.RentalCar', on_delete=models.CASCADE, null=True, blank=True, related_name='rental_car_pick')
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='picks')
    type = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.type}'