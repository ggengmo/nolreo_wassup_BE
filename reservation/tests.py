from django.test import TestCase
from rest_framework.test import APIClient

from lodging.models import Lodging, MainLocation, SubLocation, RoomType

class TestReservationLodging(TestCase):
    def setUp(self):
        self.client = APIClient()

        # 메인 지역 생성
        main_location = MainLocation.objects.create(
            address='테스트 숙소 주소'
        )

        # 서브 지역 생성
        sub_location = SubLocation.objects.create(
            main_location=main_location, 
            address='테스트 숙소 상세주소'
        )

        # 숙소 생성
        lodging = Lodging.objects.create(
            name='테스트 숙소',
            intro='테스트 숙소 소개',
            notice='테스트 숙소 주의사항',
            info='테스트 숙소 정보',
            sub_location=sub_location,
        )

        # 객실 생성
        for i in range(1, 6):
            RoomType.objects.create(
                name=f'테스트 객실{i}',
                lodging=lodging,
                price=100000,
                capacity=4,
            )
        
        # 사용자 생성 & 로그인
        data = {
            'email': 'test@gmail.com',
            'username': 'test',
            'nickname': 'test',
            'password': 'testtest1@',
            'password2': 'testtest1@',
        }
        self.client.post(
            '/account/signup/', 
            data,
            format='multipart')
        data = {
            'email': 'test@gmail.com',
            'password': 'testtest1@',
        }
        response = self.client.post(
            '/account/login/',
            data,
            format='json')
        self.access_token = response.data['access']

    def test_reservation_lodging_create(self):
        '''
        숙소 예약 생성 테스트
        1. 미로그인 상태에서 숙소 예약 생성 요청 테스트
        2. 로그인 상태에서 숙소 예약 생성 요청(1박 2일) 테스트
        3. 로그인 상태에서 숙소 예약 생성 요청(2박 3일) 테스트
        4. 이미 예약된 날짜에 숙소 예약 생성 요청 테스트
        5. 과거 날짜에 숙소 예약 생성 요청 테스트
        6. 존재하지 않는 숙소에 숙소 예약 생성 요청 테스트
        7. 예약 시작일이 예약 종료일보다 늦은 경우 테스트
        '''
        print('-- 숙소 예약 생성 테스트 BEGIN --')
        # 미로그인 상태에서 숙소 예약 생성 요청 테스트
        data = {
            'start_at': '2023-12-25',
            'end_at': '2023-12-26',
            'room': 1,
            'reservation_type': 'RO',
            'user': 1,
        }
        response = self.client.post(
            '/reservation/lodging/', 
            data, 
            format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '로그인이 필요합니다.')

        # 로그인 상태에서 숙소 예약 생성 요청(1박 2일) 테스트
        data = {
            'start_at': '2023-12-25',
            'end_at': '2023-12-26',
            'room': 1,
            'reservation_type': 'RO',
            'user': 1,
        }
        response = self.client.post(
            '/reservation/lodging/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 201)

        # 로그인 상태에서 숙소 예약 생성 요청(2박 3일) 테스트
        data = {
            'start_at': '2023-12-26',
            'end_at': '2023-12-28',
            'room': 1,
            'reservation_type': 'RO',
            'user': 1,
        }
        response = self.client.post(
            '/reservation/lodging/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # 이미 예약된 날짜에 숙소 예약 생성 요청 테스트
        data = {
            'start_at': '2023-12-25',
            'end_at': '2023-12-26',
            'room': 1,
            'reservation_type': 'RO',
            'user': 1,
        }
        response = self.client.post(
            '/reservation/lodging/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'][0], '이미 예약된 날짜입니다.')

        # 과거 날짜에 숙소 예약 생성 요청 테스트
        data = {
            'start_at': '2020-12-25',
            'end_at': '2020-12-26',
            'room': 1,
            'reservation_type': 'RO',
            'user': 1,
        }
        response = self.client.post(
            '/reservation/lodging/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'][0], '과거 날짜는 선택할 수 없습니다.')

        # 존재하지 않는 숙소에 숙소 예약 생성 요청 테스트
        data = {
            'start_at': '2023-12-25',
            'end_at': '2023-12-26',
            'room': 100,
            'reservation_type': 'RO',
            'user': 1,
        }
        response = self.client.post(
            '/reservation/lodging/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], '존재하지 않는 숙소입니다.')

        # 예약 시작일이 예약 종료일보다 늦은 경우 테스트
        data = {
            'start_at': '2023-12-26',
            'end_at': '2023-12-25',
            'room': 1,
            'reservation_type': 'RO',
            'user': 1,
        }
        response = self.client.post(
            '/reservation/lodging/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'][0], '예약 시작일이 예약 종료일보다 빨라야 합니다.')
        print('-- 숙소 예약 생성 테스트 END --')

    def test_reservation_lodging_list(self):
        '''
        숙소 예약 리스트 조회 테스트
        1. 미로그인 상태에서 숙소 예약 리스트 조회 요청 테스트
        2. 로그인 상태에서 숙소 예약이 있는 경우 리스트 조회 요청 테스트
        3. 로그인 상태에서 숙소 예약이 없는 경우 리스트 조회 요청 테스트
        '''
        print('-- 숙소 예약 리스트 조회 테스트 BEGIN --')
        # 미로그인 상태에서 숙소 예약 리스트 조회 요청 테스트
        response = self.client.get('/reservation/lodging/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '로그인이 필요합니다.')

        # 로그인 상태에서 숙소 예약이 있는 경우 리스트 조회 요청 테스트
        data = {
            'start_at': '2023-12-25',
            'end_at': '2023-12-26',
            'room': 1,
            'reservation_type': 'RO',
            'user': 1,
        }
        self.client.post(
            '/reservation/lodging/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(
            '/reservation/lodging/',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        # 로그인 상태에서 숙소 예약이 없는 경우 리스트 조회 요청 테스트
        data = {
            'email': 'test1@gmail.com',
            'username': 'test',
            'nickname': 'test1',
            'password': 'testtest1@',
            'password2': 'testtest1@',
        }
        self.client.post(
            '/account/signup/', 
            data,
            format='json')
        data = {
            'email': 'test1@gmail.com',
            'password': 'testtest1@',
        }
        response = self.client.post(
            '/account/login/',
            data,
            format='json')
        access = response.data['access']
        response = self.client.get(
            '/reservation/lodging/',
            HTTP_AUTHORIZATION=f'Bearer {access}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        print('-- 숙소 예약 리스트 조회 테스트 END --')
    