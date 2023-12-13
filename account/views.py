from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import SignupSerializer, LoginSerializer
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

        return Response({
            'refresh': str(refresh),
            'access': str(access),
        })
    

class RefreshView(TokenRefreshView):
    '''
    토큰 갱신 API
    '''
    def post(self, request: Request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


signup = SignupView.as_view()
login = LoginView.as_view()
refresh = RefreshView.as_view()