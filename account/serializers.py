from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.validators import MinLengthValidator, MaxLengthValidator

from .models import CustomUser as User

class SignupSerializer(ModelSerializer):
    '''
    회원가입 serializer
    '''
    password = serializers.CharField(
        style={'input_type': 'password'}, 
        write_only=True,
        validators=[MinLengthValidator(8, '비밀번호는 8글자 이상 15글자 이하로 입력해주세요.'), MaxLengthValidator(15, '비밀번호는 8글자 이상 15글자 이하로 입력해주세요.')],
    )
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'nickname', 'password', 'password2', 'image']
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def create(self, validated_data):
        '''
        사용자 생성 메서드
        '''
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            nickname=validated_data['nickname'],
        )
        if validated_data.get('image'):
            user.image = validated_data['image']
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def validate_password(self, value):
        '''
        비밀번호 유효성 검사 메서드
        '''
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("비밀번호는 숫자를 포함해야 합니다.")
        
        if not any(char in '!@#$%^&*()_+' for char in value):
            raise serializers.ValidationError("비밀번호는 특수문자를 포함해야 합니다.")
        
        password2 = self.initial_data.get('password2')
        if value != password2:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return value
    

class LoginSerializer(TokenObtainPairSerializer):
    '''
    로그인 serializer
    '''
    username_field = 'email'

    default_error_messages = {
        'no_active_account': '이메일 또는 비밀번호가 일치하지 않습니다.',
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field].error_messages['required'] = '이메일을 입력해주세요.'
        self.fields['password'].error_messages['required'] = '비밀번호를 입력해주세요.'

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = self.user
        return data


class UserSerializer(ModelSerializer):
    '''
    사용자 정보 serializer
    '''
    class Meta:
        model = User
        fields = ['email', 'username', 'nickname', 'image']
        read_only_fields = ['email', 'username']


    def validate_nickname(self, value):
        '''
        닉네임 유효성 검사 메서드
        '''
        if self.instance.nickname == value:
            raise serializers.ValidationError('이전 별명과 같습니다.')
        if not value:
            raise serializers.ValidationError('별명을 입력해주세요.')
        return value
    

class PasswordSerializer(ModelSerializer):
    '''
    비밀번호 변경 serializer
    '''
    old_password = serializers.CharField(
        style={'input_type': 'password'}, 
        write_only=True,
    )
    password = serializers.CharField(
        style={'input_type': 'password'}, 
        write_only=True,
        validators=[MinLengthValidator(8, '비밀번호는 8글자 이상 15글자 이하로 입력해주세요.'), MaxLengthValidator(15, '비밀번호는 8글자 이상 15글자 이하로 입력해주세요.')],
    )
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['old_password', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def update(self, instance, validated_data):
        '''
        비밀번호 변경 메서드
        '''
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    
    def validate_password(self, value):
        '''
        비밀번호 유효성 검사 메서드
        '''
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("비밀번호는 숫자를 포함해야 합니다.")
        
        if not any(char in '!@#$%^&*()_+' for char in value):
            raise serializers.ValidationError("비밀번호는 특수문자를 포함해야 합니다.")
        
        password2 = self.initial_data.get('password2')
        if value != password2:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return value
    
    def validate_old_password(self, value):
        '''
        기존 비밀번호 유효성 검사 메서드
        '''
        if not self.instance.check_password(value):
            raise serializers.ValidationError("기존 비밀번호가 일치하지 않습니다.")
        return value
    
    