from rest_framework.generics import CreateAPIView
from .serializers import BusSerializer, TrianSerializer

class BusView(CreateAPIView):
    '''
    버스 생성 API
    '''
    serializer_class = BusSerializer

bus = BusView.as_view()


class TrainView(CreateAPIView):
    '''
    기차 생성 API
    '''
    serializer_class = TrianSerializer

train = TrainView.as_view()