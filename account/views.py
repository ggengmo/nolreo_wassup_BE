from rest_framework.generics import CreateAPIView

from .serializers import SignupSerializer
class SignupView(CreateAPIView):
    '''
    회원가입 API
    '''
    serializer_class = SignupSerializer


signup = SignupView.as_view()