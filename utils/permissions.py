from rest_framework import permissions
from rest_framework.request import Request
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated

class CustomIsAuthenticated(IsAuthenticated):
    '''
    인증 여부 확인 메서드
        - 에러 메시지 변경
    '''
    def has_permission(self, request: Request, view) -> bool:
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            raise AuthenticationFailed('로그인이 필요합니다.')
        return is_authenticated

class CustomJWTAuthentication(JWTAuthentication):
    
    def authenticate(self, request: Request):
        '''
        토큰 인증 메서드
            - 에러 메시지 변경
        '''
        try:
            auth = super().authenticate(request)
        except TokenError as e:
            raise AuthenticationFailed('유효하지 않은 토큰입니다.')
        return super().authenticate(request)


class IsOwner(permissions.BasePermission):
    message = '권한이 없습니다.'

    def has_object_permission(self, request, view, obj):
        return obj == request.user