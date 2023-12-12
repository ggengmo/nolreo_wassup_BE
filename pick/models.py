from django.db import models

class Pick(models.Model):
    '''
    사용자 찜 모델
    '''
    lodging_id = models.ForeignKey('lodging.Lodging', on_delete=models.CASCADE, null=True, blank=True, related_name='lodging_pick')
    bus_id = models.ForeignKey('traffic.Bus', on_delete=models.CASCADE, null=True, blank=True, related_name='bus_pick')
    train_id = models.ForeignKey('traffic.Train', on_delete=models.CASCADE, null=True, blank=True, related_name='train_pick')
    rental_car_id = models.ForeignKey('traffic.RentalCar', on_delete=models.CASCADE, null=True, blank=True, related_name='rental_car_pick')
    user_id = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)