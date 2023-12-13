from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser
from .serializers import BusSerializer, TrianSerializer

class BusView(CreateAPIView):
    '''
    버스 생성 API
    '''
    serializer_class = BusSerializer
    permission_classes = [IsAdminUser]

bus = BusView.as_view()


class TrainView(CreateAPIView):
    '''
    기차 생성 API
    '''
    serializer_class = TrianSerializer
    permission_classes = [IsAdminUser]

train = TrainView.as_view()