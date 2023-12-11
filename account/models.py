from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser


class CustomUser(AbstractBaseUser):
    '''
    사용자 모델
    '''
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile_image', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email