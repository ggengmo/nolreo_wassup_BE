from django.test import TestCase
from rest_framework.test import APIClient

class TestTrafficCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_bus_create(self):
        '''
        버스 생성 테스트
        '''
        print('-- 버스 생성 테스트 BEGIN --')
        # 정상 처리 테스트
        bus_data = {
            'depart_point': '서울',
            'dest_point': '부산',
            'depart_time': '2023-12-15 12:00:00',
            'arrival_time': '2023-12-15 15:00:00',
            'num': '1234',
        }
        response = self.client.post('/traffic/bus/', bus_data, format='json')
        self.assertEqual(response.status_code, 201)

        # 비정상 처리 테스트 - 출발지와 도착지가 같을 경우
        bus_data = {
            'depart_point': '서울',
            'dest_point': '서울',
            'depart_time': '2023-12-12 12:00:00',
            'arrival_time': '2023-12-12 15:00:00',
            'num': '1234',
        }
        response = self.client.post('/traffic/bus/', bus_data, format='json')
        self.assertEqual(response.status_code, 400)
        # 비정상 처리 테스트 - 출발시간이 도착시간보다 늦을 경우
        bus_data = {
            'depart_point': '서울',
            'dest_point': '부산',
            'depart_time': '2023-12-12 16:00:00',
            'arrival_time': '2023-12-12 15:00:00',
            'num': '1234',
        }
        response = self.client.post('/traffic/bus/', bus_data, format='json')
        self.assertEqual(response.status_code, 400)
        # 비정상 처리 테스트 - 출발시간이 현재시간보다 빠를 경우
        current_time = '2023-12-12 10:00:00'
        bus_data = {
            'depart_point': '서울',
            'dest_point': '서울',
            'depart_time': '2023-12-12 09:00:00',
            'arrival_time': '2023-12-12 15:00:00',
            'num': '1234',
        }
        response = self.client.post('/traffic/bus/', bus_data, format='json')
        self.assertEqual(response.status_code, 400)
        # 비정상 처리 테스트 - 도착시간이 현재시간보다 빠를 경우
        current_time = '2023-12-12 10:00:00'
        bus_data = {
            'depart_point': '서울',
            'dest_point': '부산',
            'depart_time': '2023-12-12 09:00:00',
            'arrival_time': '2023-12-12 09:30:00',
            'num': '1234',
        }
        response = self.client.post('/traffic/bus/', bus_data, format='json')
        self.assertEqual(response.status_code, 400)
        # 비정상 처리 테스트 - 출발시간이 현재시간과 같을 경우
        current_time = '2023-12-12 10:00:00'
        bus_data = {
            'depart_point': '서울',
            'dest_point': '부산',
            'depart_time': '2023-12-12 10:00:00',
            'arrival_time': '2023-12-12 10:30:00',
            'num': '1234',
        }
        response = self.client.post('/traffic/bus/', bus_data, format='json')
        self.assertEqual(response.status_code, 400)
        # 비정상 처리 테스트 - 도착시간이 현재시간과 같을 경우
        current_time = '2023-12-12 10:00:00'
        bus_data = {
            'depart_point': '서울',
            'dest_point': '부산',
            'depart_time': '2023-12-12 09:00:00',
            'arrival_time': '2023-12-12 10:00:00',
            'num': '1234',
        }
        response = self.client.post('/traffic/bus/', bus_data, format='json')
        self.assertEqual(response.status_code, 400)
        print('-- 버스 생성 테스트 END --')