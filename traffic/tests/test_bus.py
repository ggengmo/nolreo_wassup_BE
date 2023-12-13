from django.test import TestCase
from rest_framework.test import APIClient

from account.models import CustomUser as User

class TestBusCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email = 'test1@gmail.com',
            password = 'testtest1@',
        )
        self.user = User.objects.create_user(
            email = 'test2@gmail.com',
            password = 'testtest2@',
            nickname = 'test2',
        )

    def test_admin_login(self):
        '''
        어드민 로그인 테스트
        '''
        print('-- 어드민 로그인 테스트 BEGIN --')
        self.client.force_login(self.admin)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        print('-- 어드민 로그인 테스트 END --')

    def test_user_login(self):
        '''
        사용자 로그인 테스트
        '''
        print('-- 사용자 로그인 테스트 BEGIN --')
        self.client.force_login(self.user)
        response = self.client.get('/traffic/bus/')
        self.assertEqual(response.status_code, 401)
        print('-- 사용자 로그인 테스트 END --')

    def test_bus_create_admin(self):
        '''
        버스 생성 테스트
        '''
        print('-- 버스 생성 테스트 BEGIN --')
        # 정상 처리 테스트
        self.client.force_authenticate(user=self.admin)
        bus_data = {
            'depart_point': '서울',
            'dest_point': '부산',
            'depart_time': '2023-12-15 12:00:00',
            'arrival_time': '2023-12-15 15:00:00',
            'num': '1234',
            'price': '10000',
        }
        response = self.client.post('/traffic/bus/', bus_data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 201)

        # 비정상 처리 테스트 - 출발지와 도착지가 같을 경우
        bus_data = {
            'depart_point': '서울',
            'dest_point': '서울',
            'depart_time': '2023-12-12 12:00:00',
            'arrival_time': '2023-12-12 15:00:00',
            'num': '1234',
            'price': '10000',
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
            'price': '10000',
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
            'price': '10000',
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
            'price': '10000',
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
            'price': '10000',
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
            'price': '10000',
        }
        response = self.client.post('/traffic/bus/', bus_data, format='json')
        self.assertEqual(response.status_code, 400)
        print('-- 버스 생성 테스트 END --')

    def test_bus_create_user(self):
        '''
        버스 생성 테스트
        '''
        print('-- 버스 생성 테스트 BEGIN --')
        # 정상 처리 테스트
        self.client.force_login(user=self.user)
        bus_data = {
            'depart_point': '서울',
            'dest_point': '부산',
            'depart_time': '2023-12-15 12:00:00',
            'arrival_time': '2023-12-15 15:00:00',
            'num': '1234',
            'price': '10000',
        }
        response = self.client.post('/traffic/bus/', bus_data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 401)

        print('-- 버스 생성 테스트 END --')
