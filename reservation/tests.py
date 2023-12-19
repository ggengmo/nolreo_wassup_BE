from django.test import TestCase
from rest_framework.test import APIClient

from lodging.models import Lodging, MainLocation, SubLocation, RoomType
from traffic.models import Bus, Train

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
            'start_at': '2024-12-25',
            'end_at': '2024-12-26',
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
            'start_at': '2024-12-25',
            'end_at': '2024-12-26',
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
            'start_at': '2024-12-26',
            'end_at': '2024-12-28',
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
            'start_at': '2024-12-25',
            'end_at': '2024-12-26',
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
            'start_at': '2024-12-25',
            'end_at': '2024-12-26',
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
            'start_at': '2024-12-26',
            'end_at': '2024-12-25',
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
        data = {
            'start_at': '2024-12-25',
            'end_at': '2024-12-26',
            'room': 1,
            'reservation_type': 'RO',
            'user': 1,
        }
        self.client.post(
            '/reservation/lodging/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        # 미로그인 상태에서 숙소 예약 리스트 조회 요청 테스트
        response = self.client.get('/reservation/lodging/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '로그인이 필요합니다.')

        # 로그인 상태에서 숙소 예약이 있는 경우 리스트 조회 요청 테스트
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
    
    def test_reservation_lodging_patch(self):
        '''
        숙소 예약 수정 테스트
        1. 미로그인 상태에서 숙소 예약 수정 요청 테스트
        2. 로그인 상태(권한 X)에서 숙소 예약 수정 요청 테스트
        3. 로그인 상태(권한 O)에서 숙소 예약 수정 요청 테스트
        4. 이전 예약 날짜와 같은 예약 날짜로 수정 요청 테스트
        5. 예약 시작일이 예약 종료일보다 늦은 경우 테스트
        6. 예약 시작일이 예약 종료일과 같은 경우 테스트
        7. 예약 시작일이 과거 날짜인 경우 테스트
        8. 존재하지 않는 숙소에 예약 수정 요청 테스트
        9. 예약된 날짜에 예약 수정 요청 테스트
        '''
        print('-- 숙소 예약 수정 테스트 BEGIN --')
        data = {
            'start_at': '2024-12-25',
            'end_at': '2024-12-26',
            'room': 1,
            'reservation_type': 'RO',
            'user': 1,
        }
        self.client.post(
            '/reservation/lodging/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        # 미로그인 상태에서 숙소 예약 수정 요청 테스트
        data = {
            'start_at': '2024-12-27',
            'end_at': '2024-12-28',
            'room': 1,
        }
        response = self.client.patch(
            '/reservation/lodging/1/', 
            data, 
            format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '로그인이 필요합니다.')

        # 로그인 상태(권한 X)에서 숙소 예약 수정 요청 테스트
        signup_data = {
            'email': 'test1@gmail.com',
            'username': 'test',
            'nickname': 'test1',
            'password': 'testtest1@',
            'password2': 'testtest1@',
        }
        self.client.post(
            '/account/signup/', 
            signup_data,
            format='json')
        login_data = {
            'email': 'test1@gmail.com',
            'password': 'testtest1@',
        }
        response = self.client.post(
            '/account/login/',
            login_data,
            format='json')
        access = response.data['access']
        response = self.client.patch(
            '/reservation/lodging/1/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {access}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], '해당 숙소를 예약한 기록이 없습니다.')

        # 로그인 상태(권한 O)에서 숙소 예약 수정 요청 테스트
        response = self.client.patch(
            '/reservation/lodging/1/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)

        # 이전 예약 날짜와 같은 예약 날짜로 수정 요청 테스트
        response = self.client.patch(
            '/reservation/lodging/1/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'][0], '이전 예약 날짜와 같은 예약 날짜입니다.')

        # 예약 시작일이 예약 종료일보다 늦은 경우 테스트
        data = {
            'start_at': '2024-12-28',
            'end_at': '2024-12-27',
            'room': 1,
        }
        response = self.client.patch(
            '/reservation/lodging/1/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'][0], '예약 시작일이 예약 종료일보다 빨라야 합니다.')

        # 예약 시작일이 예약 종료일과 같은 경우 테스트
        data = {
            'start_at': '2024-12-28',
            'end_at': '2024-12-28',
            'room': 1,
        }
        response = self.client.patch(
            '/reservation/lodging/1/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'][0], '예약 시작일이 예약 종료일보다 빨라야 합니다.')

        # 예약 시작일이 과거 날짜인 경우 테스트
        data = {
            'start_at': '2020-12-28',
            'end_at': '2020-12-29',
            'room': 1,
        }
        response = self.client.patch(
            '/reservation/lodging/1/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'][0], '과거 날짜는 선택할 수 없습니다.')

        # 존재하지 않는 숙소에 예약 수정 요청 테스트
        data = {
            'start_at': '2024-12-28',
            'end_at': '2024-12-29',
            'room': 1,
        }
        response = self.client.patch(
            '/reservation/lodging/100/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], '해당 숙소를 예약한 기록이 없습니다.')

        # 예약된 날짜에 예약 수정 요청 테스트
        data = {
            'start_at': '2024-12-28',
            'end_at': '2024-12-29',
            'room': 1,
        }
        self.client.post(
            '/reservation/lodging/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {access}')
        response = self.client.patch(
            '/reservation/lodging/1/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'][0], '이미 예약된 날짜입니다.')
        print('-- 숙소 예약 수정 테스트 END --')

    def test_reservation_lodging_delete(self):
        '''
        숙소 예약 삭제 테스트
        1. 미로그인 상태에서 숙소 예약 삭제 요청 테스트
        2. 로그인 상태(권한 X)에서 숙소 예약 삭제 요청 테스트
        3. 로그인 상태(권한 O)에서 숙소 예약 삭제 요청 테스트
        4. 존재하지 않는 숙소 예약 삭제 요청 테스트
        '''
        print('-- 숙소 예약 삭제 테스트 BEGIN --')
        data = {
            'start_at': '2024-12-25',
            'end_at': '2024-12-26',
            'room': 1,
            'reservation_type': 'RO',
            'user': 1,
        }
        self.client.post(
            '/reservation/lodging/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        # 미로그인 상태에서 숙소 예약 삭제 요청 테스트
        response = self.client.delete('/reservation/lodging/1/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '로그인이 필요합니다.')

        # 로그인 상태(권한 X)에서 숙소 예약 삭제 요청 테스트
        signup_data = {
            'email': 'test1@gmail.com',
            'username': 'test',
            'nickname': 'test1',
            'password': 'testtest1@',
            'password2': 'testtest1@',
        }
        self.client.post(
            '/account/signup/', 
            signup_data,
            format='json')
        login_data = {
            'email': 'test1@gmail.com',
            'password': 'testtest1@',
        }
        response = self.client.post(
            '/account/login/',
            login_data,
            format='json')
        access = response.data['access']
        response = self.client.delete(
            '/reservation/lodging/1/', 
            HTTP_AUTHORIZATION=f'Bearer {access}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], '해당 숙소를 예약한 기록이 없습니다.')

        # 로그인 상태(권한 O)에서 숙소 예약 삭제 요청 테스트
        response = self.client.delete(
            '/reservation/lodging/1/', 
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 204)

        # 존재하지 않는 숙소 예약 삭제 요청 테스트
        response = self.client.delete(
            '/reservation/lodging/1/', 
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], '해당 숙소를 예약한 기록이 없습니다.')
        print('-- 숙소 예약 삭제 테스트 END --')


class TestReservationBus(TestCase):
    def setUp(self):
        self.client = APIClient()

        # 버스 생성
        for i in range(1, 6):
            Bus.objects.create(
                depart_point = '서울',
                dest_point = '부산',
                depart_time = f'2024-12-25 12:20:00',
                arrival_time = f'2024-12-25 15:20:00',
                num = f'{1234 + i}',
                price = '10000',
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

    def test_reservation_bus_create(self):
        '''
        버스 예약 생성 테스트
        1. 미로그인 상태에서 버스 예약 생성 요청 테스트
        2. 로그인 상태에서 버스 예약 생성 요청 테스트
        3. 이미 만원인 버스 예약 생성 요청 테스트
        4. 과거 날짜에 버스 예약 생성 요청 테스트
        5. 존재하지 않는 버스에 버스 예약 생성 요청 테스트
        6. 여러 좌석을 예약했을 때 예약 가능한 경우 테스트
        7. 여러 좌석을 예약했을 때 좌석이 부족한 경우 테스트
        '''
        print('-- 버스 예약 생성 테스트 BEGIN --')
        # 미로그인 상태에서 버스 예약 생성 요청 테스트
        data = {
            'bus': 1,
            'reservation_type': 'BU',
            'user': 1,
            'seat': 1,
        }
        response = self.client.post(
            '/reservation/bus/', 
            data, 
            format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '로그인이 필요합니다.')

        # 로그인 상태에서 버스 예약 생성 요청 테스트
        response = self.client.post(
            '/reservation/bus/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 201)

        # 이미 만원인 버스 예약 생성 요청 테스트
        for _ in range(39):
            self.client.post(
                '/reservation/bus/', 
                data, 
                format='json',
                HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(
            '/reservation/bus/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertIn('예약이 불가능합니다.', response.data['message'][0])
        
        # 과거 날짜에 버스 예약 생성 요청 테스트
        Bus.objects.create(
            depart_point = '서울',
            dest_point = '부산',
            depart_time = '2022-12-25 12:20:00',
            arrival_time = '2022-12-25 15:20:00',
            num = '5678',
            price = '10000',
        )
        data = {
            'bus': 6,
            'reservation_type': 'BU',
            'user': 1,
            'seat': 1,
        }
        response = self.client.post(
            '/reservation/bus/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'][0], '과거 버스는 예약할 수 없습니다.')

        # 존재하지 않는 버스에 버스 예약 생성 요청 테스트
        data = {
            'bus': 100,
            'reservation_type': 'BU',
            'user': 1,
            'seat': 1,
        }
        response = self.client.post(
            '/reservation/bus/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], '존재하지 않는 버스입니다.')

        # 여러 좌석을 예약했을 때 예약 가능한 경우 테스트
        data = {
            'bus': 2,
            'reservation_type': 'BU',
            'user': 1,
            'seat': 2,
        }
        response = self.client.post(
            '/reservation/bus/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 201)

        # 여러 좌석을 예약했을 때 좌석이 부족한 경우 테스트
        data = {
            'bus': 2,
            'reservation_type': 'BU',
            'user': 1,
            'seat': 40,
        }
        response = self.client.post(
            '/reservation/bus/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertIn('예약이 불가능합니다.', response.data['message'][0])
        print('-- 버스 예약 생성 테스트 END --')

    def test_reservation_bus_list(self):
        '''
        버스 예약 리스트 조회 테스트
        1. 미로그인 상태에서 버스 예약 리스트 조회 요청 테스트
        2. 로그인 상태에서 버스 예약이 있는 경우 리스트 조회 요청 테스트
        3. 로그인 상태에서 버스 예약이 없는 경우 리스트 조회 요청 테스트
        '''
        print('-- 버스 예약 리스트 조회 테스트 BEGIN --')
        data = {
            'bus': 1,
            'reservation_type': 'BU',
            'user': 1,
            'seat': 1,
        }
        self.client.post(
            '/reservation/bus/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        # 미로그인 상태에서 버스 예약 리스트 조회 요청 테스트
        response = self.client.get('/reservation/bus/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '로그인이 필요합니다.')

        # 로그인 상태에서 버스 예약이 있는 경우 리스트 조회 요청 테스트
        response = self.client.get(
            '/reservation/bus/',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        # 로그인 상태에서 버스 예약이 없는 경우 리스트 조회 요청 테스트
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
            '/reservation/bus/',
            HTTP_AUTHORIZATION=f'Bearer {access}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        print('-- 버스 예약 리스트 조회 테스트 END --')

    def test_reservation_bus_delete(self):
        '''
        버스 예약 삭제 테스트
        1. 미로그인 상태에서 버스 예약 삭제 요청 테스트
        2. 로그인 상태(권한 X)에서 버스 예약 삭제 요청 테스트
        3. 로그인 상태(권한 O)에서 버스 예약 삭제 요청 테스트
        4. 존재하지 않는 버스 예약 삭제 요청 테스트
        '''
        print('-- 버스 예약 삭제 테스트 BEGIN --')
        data = {
            'bus': 1,
            'reservation_type': 'BU',
            'user': 1,
            'seat': 1,
        }
        self.client.post(
            '/reservation/bus/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        # 미로그인 상태에서 버스 예약 삭제 요청 테스트
        response = self.client.delete('/reservation/bus/1/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '로그인이 필요합니다.')

        # 로그인 상태(권한 X)에서 버스 예약 삭제 요청 테스트
        signup_data = {
            'email': 'test1@gmail.com',
            'username': 'test',
            'nickname': 'test1',
            'password': 'testtest1@',
            'password2': 'testtest1@',
        }
        self.client.post(
            '/account/signup/', 
            signup_data,
            format='json')
        login_data = {
            'email': 'test1@gmail.com',
            'password': 'testtest1@',
        }
        response = self.client.post(
            '/account/login/',
            login_data,
            format='json')
        access = response.data['access']
        response = self.client.delete(
            '/reservation/bus/1/', 
            HTTP_AUTHORIZATION=f'Bearer {access}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], '해당 버스를 예약한 기록이 없습니다.')

        # 로그인 상태(권한 O)에서 버스 예약 삭제 요청 테스트
        response = self.client.delete(
            '/reservation/bus/1/', 
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 204)

        # 존재하지 않는 버스 예약 삭제 요청 테스트
        response = self.client.delete(
            '/reservation/bus/1/', 
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], '해당 버스를 예약한 기록이 없습니다.')
        print('-- 버스 예약 삭제 테스트 END --')


class TestReservationTrain(TestCase):
    def setUp(self):
        self.client = APIClient()

        # 기차 생성
        for i in range(1, 6):
            Train.objects.create(
                depart_point = '서울',
                dest_point = '부산',
                depart_time = f'2024-12-15 12:{i + 20}:00',
                arrival_time = f'2024-12-15 15:{i + 20}:00',
                num = f'{1234 + i}',
                price = '10000',
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

    def test_reservation_train_create(self):
        '''
        기차 예약 생성 테스트
        1. 미로그인 상태에서 기차 예약 생성 요청 테스트
        2. 로그인 상태에서 기차 예약 생성 요청 테스트
        3. 이미 만원인 버스 기차 생성 요청 테스트
        4. 과거 날짜에 버스 기차 생성 요청 테스트
        5. 존재하지 않는 기차에 버스 예약 생성 요청 테스트
        6. 여러 좌석을 예약했을 때 예약 가능한 경우 테스트
        7. 여러 좌석을 예약했을 때 좌석이 부족한 경우 테스트
        '''
        print('-- 기차 예약 생성 테스트 BEGIN --')
        # 미로그인 상태에서 기차 예약 생성 요청 테스트
        data = {
            'train': 1,
            'reservation_type': 'TR',
            'user': 1,
            'seat': 1,
        }
        response = self.client.post(
            '/reservation/train/', 
            data, 
            format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '로그인이 필요합니다.')

        # 로그인 상태에서 기차 예약 생성 요청 테스트
        response = self.client.post(
            '/reservation/train/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 201)

        # 이미 만원인 기차 예약 생성 요청 테스트
        for _ in range(399):
            self.client.post(
                '/reservation/train/', 
                data, 
                format='json',
                HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(
            '/reservation/train/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertIn('예약이 불가능합니다.', response.data['message'][0])
        
        # 과거 날짜에 기차 예약 생성 요청 테스트
        Train.objects.create(
            depart_point = '서울',
            dest_point = '부산',
            depart_time = '2022-12-15 12:20:00',
            arrival_time = f'2022-12-15 15:20:00',
            num = '1234',
            price = '10000',
        )
        data = {
            'train': 6,
            'reservation_type': 'TR',
            'user': 1,
            'seat': 1,
        }
        response = self.client.post(
            '/reservation/train/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'][0], '과거 기차는 예약할 수 없습니다.')

        # 존재하지 않는 기차에 기차 예약 생성 요청 테스트
        data = {
            'train': 100,
            'reservation_type': 'TR',
            'user': 1,
            'seat': 1,
        }
        response = self.client.post(
            '/reservation/train/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], '존재하지 않는 기차입니다.')

        # 여러 좌석을 예약했을 때 예약 가능한 경우 테스트
        data = {
            'train': 2,
            'reservation_type': 'TR',
            'user': 1,
            'seat': 2,
        }
        response = self.client.post(
            '/reservation/train/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 201)

        # 여러 좌석을 예약했을 때 좌석이 부족한 경우 테스트
        data = {
            'train': 2,
            'reservation_type': 'TR',
            'user': 1,
            'seat': 400,
        }
        response = self.client.post(
            '/reservation/train/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertIn('예약이 불가능합니다.', response.data['message'][0])
        print('-- 기차 예약 생성 테스트 END --')

    def test_reservation_train_list(self):
        '''
        기차 예약 리스트 조회 테스트
        1. 미로그인 상태에서 기차 예약 리스트 조회 요청 테스트
        2. 로그인 상태에서 기차 예약이 있는 경우 리스트 조회 요청 테스트
        3. 로그인 상태에서 기차 예약이 없는 경우 리스트 조회 요청 테스트
        '''
        print('-- 기차 예약 리스트 조회 테스트 BEGIN --')
        data = {
            'train': 1,
            'reservation_type': 'TR',
            'user': 1,
            'seat': 1,
        }
        response = self.client.post(
            '/reservation/train/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        # 미로그인 상태에서 기차 예약 리스트 조회 요청 테스트
        response = self.client.get('/reservation/train/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '로그인이 필요합니다.')

        # 로그인 상태에서 기차 예약이 있는 경우 리스트 조회 요청 테스트
        response = self.client.get(
            '/reservation/train/',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        # 로그인 상태에서 기차 예약이 없는 경우 리스트 조회 요청 테스트
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
            '/reservation/train/',
            HTTP_AUTHORIZATION=f'Bearer {access}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        print('-- 기차 예약 리스트 조회 테스트 END --')

    def test_reservation_train_delete(self):
        '''
        기차 예약 삭제 테스트
        1. 미로그인 상태에서 기차 예약 삭제 요청 테스트
        2. 로그인 상태(권한 X)에서 기차 예약 삭제 요청 테스트
        3. 로그인 상태(권한 O)에서 기차 예약 삭제 요청 테스트
        4. 존재하지 않는 기차 예약 삭제 요청 테스트
        '''
        print('-- 기차 예약 삭제 테스트 BEGIN --')
        data = {
            'train': 1,
            'reservation_type': 'TR',
            'user': 1,
            'seat': 1,
        }
        response = self.client.post(
            '/reservation/train/', 
            data, 
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        # 미로그인 상태에서 기차 예약 삭제 요청 테스트
        response = self.client.delete('/reservation/train/1/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '로그인이 필요합니다.')

        # 로그인 상태(권한 X)에서 기차 예약 삭제 요청 테스트
        signup_data = {
            'email': 'test1@gmail.com',
            'username': 'test',
            'nickname': 'test1',
            'password': 'testtest1@',
            'password2': 'testtest1@',
        }
        self.client.post(
            '/account/signup/', 
            signup_data,
            format='json')
        login_data = {
            'email': 'test1@gmail.com',
            'password': 'testtest1@',
        }
        response = self.client.post(
            '/account/login/',
            login_data,
            format='json')
        access = response.data['access']
        response = self.client.delete(
            '/reservation/train/1/', 
            HTTP_AUTHORIZATION=f'Bearer {access}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], '해당 기차를 예약한 기록이 없습니다.')

        # 로그인 상태(권한 O)에서 버스 예약 삭제 요청 테스트
        response = self.client.delete(
            '/reservation/train/1/', 
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 204)

        # 존재하지 않는 기차 예약 삭제 요청 테스트
        response = self.client.delete(
            '/reservation/train/1/', 
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], '해당 기차를 예약한 기록이 없습니다.')
        print('-- 기차 예약 삭제 테스트 END --')

