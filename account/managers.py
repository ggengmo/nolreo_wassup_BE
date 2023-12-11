from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extrafields):
        '''
        email을 로그인 수단으로 사용하기 위한
        user custom manager
        '''
        if not email:
            raise ValueError('Email은 필수 값입니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extrafields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extrafields):
        '''
        email을 로그인 수단으로 사용하기 위한
        superuser custom manager
        '''
        extrafields.setdefault('is_staff', True)
        extrafields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extrafields)
