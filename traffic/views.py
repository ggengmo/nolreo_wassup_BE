from rest_framework.generics import CreateAPIView
from .serializers import BusSerializer

class BusView(CreateAPIView):
    '''
    버스 생성 API
    '''
    serializer_class = BusSerializer

bus = BusView.as_view()
