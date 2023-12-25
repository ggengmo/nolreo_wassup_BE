from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from .models import CustomUser as User
from utils.permissions import CustomJWTAuthentication, CustomIsAuthenticated, IsOwner
from .serializers import SignupSerializer, LoginSerializer, UserSerializer, PasswordSerializer

class SignupView(CreateAPIView):
    '''
    회원가입 API
    '''
    serializer_class = SignupSerializer

    @extend_schema(
        request=SignupSerializer,
        responses={200: SignupSerializer(many=False)}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginView(TokenObtainPairView):
    '''
    로그인 API
    '''
    serializer_class = LoginSerializer

    @extend_schema(
        request=LoginSerializer,
        responses={200: OpenApiTypes.OBJECT}
    )
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
    

class UserView(ModelViewSet):
    '''
    유저 정보 API
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [CustomIsAuthenticated, IsOwner]
    authentication_classes = [CustomJWTAuthentication]
    

class PasswordView(UpdateAPIView):
    '''
    비밀번호 변경 API
    '''
    queryset = User.objects.all()
    serializer_class = PasswordSerializer
    permission_classes = [CustomIsAuthenticated, IsOwner]
    authentication_classes = [CustomJWTAuthentication]
    http_method_names = ['patch']
    

signup = SignupView.as_view()
login = LoginView.as_view()
user = UserView.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})
password = PasswordView.as_view()