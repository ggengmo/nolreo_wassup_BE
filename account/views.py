from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import CustomUser as User
from utils.permissions import CustomJWTAuthentication, CustomIsAuthenticated, IsOwner
from .serializers import SignupSerializer, LoginSerializer, UserSerializer, PasswordSerializer

class SignupView(CreateAPIView):
    '''
    회원가입 API
    '''
    serializer_class = SignupSerializer


class LoginView(TokenObtainPairView):
    '''
    로그인 API
    '''
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.validated_data['refresh']
        access = serializer.validated_data['access']
        user = serializer.validated_data['user']

        return Response({
            'user_id': user.id,
            'refresh': str(refresh),
            'access': str(access),
        })
    

class RefreshView(TokenRefreshView):
    '''
    토큰 갱신 API
    '''
    def post(self, request: Request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class UserView(ModelViewSet):
    '''
    유저 정보 API
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [CustomIsAuthenticated, IsOwner]
    authentication_classes = [CustomJWTAuthentication]

    def get_object(self):
        return super().get_object()
    

class PasswordView(UpdateAPIView):
    '''
    비밀번호 변경 API
    '''
    queryset = User.objects.all()
    serializer_class = PasswordSerializer
    permission_classes = [CustomIsAuthenticated, IsOwner]
    authentication_classes = [CustomJWTAuthentication]
    http_method_names = ['patch']

    def get_object(self):
        return super().get_object()

signup = SignupView.as_view()
login = LoginView.as_view()
refresh = RefreshView.as_view()
user = UserView.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})
password = PasswordView.as_view()