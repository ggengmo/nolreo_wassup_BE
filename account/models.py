from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser

class CustomUser(AbstractBaseUser):
    '''
    사용자 모델
    '''
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True, error_messages={'unique': '이미 사용중인 이메일입니다.'})
    nickname = models.CharField(max_length=100, unique=True, error_messages={'unique': '이미 사용중인 별명입니다.'})
    image = models.ImageField(upload_to='profile_image/%Y/%m/%d/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email
    
    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def has_perm(self, obj=None):
        return self.is_superuser