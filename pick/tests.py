from django.test import TestCase
from rest_framework.test import APIClient

from lodging.models import Lodging, SubLocation, MainLocation
from .models import Pick

class TestPick(TestCase):
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
        for _ in range(1, 6):
            Lodging.objects.create(
                name='테스트 숙소',
                intro='테스트 숙소 소개',
                notice='테스트 숙소 주의사항',
                info='테스트 숙소 정보',
                sub_location=sub_location,
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

    def test_pick_lodging_create(self):
        '''
        숙소 찜 생성 테스트
        1. 미로그인 상태에서 숙소 찜 생성 요청 테스트
        2. 로그인 상태에서 숙소 찜 생성 요청 테스트
        3. 중복 생성 요청 테스트
        '''
        print('-- 숙소 찜 생성 테스트 BEGIN --')
        # 미로그인 상태에서 숙소 찜 생성 요청
        data = {
            'lodging': 1,
            'pick_type': 'LG',
            'user': 1,
        }
        response = self.client.post(
            '/pick/lodging/',
            data=data,
            format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '로그인이 필요합니다.')

        # 로그인 상태에서 숙소 찜 생성 요청
        response = self.client.post(
            '/pick/lodging/',
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['lodging'], 1)
        self.assertEqual(response.data['pick_type'], 'LG')
        self.assertEqual(Pick.objects.all().count(), 1)

        # 중복 생성 요청
        response = self.client.post(
            '/pick/lodging/',
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], '이미 찜한 숙소입니다.')
        print('-- 숙소 찜 생성 테스트 END --')

    def test_pick_lodging_list(self):
        '''
        숙소 찜 리스트 조회 테스트
        1. 미로그인 상태에서 숙소 찜 리스트 조회 요청 테스트
        2. 로그인 상태에서 본인 숙소 찜 리스트 조회 요청 테스트
        '''
        print('-- 숙소 찜 리스트 조회 테스트 BEGIN --')
        data = {
            'user':1,
            'pick_type': 'LG',
        }
        for i in range(1, 6):
            self.client.post(
                '/pick/lodging/',
                data={
                    'lodging': i,
                    'pick_type': 'LG',
                    'user': 1,},
                HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
                format='json')
        # 미로그인 상태에서 숙소 찜 리스트 조회 요청
        response = self.client.get(
            '/pick/lodging/',
            data=data,
            format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '로그인이 필요합니다.')

        # 로그인 상태에서 본인 숙소 찜 리스트 조회 요청
        response = self.client.get(
            '/pick/lodging/',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            data=data,
            format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)
        print('-- 숙소 찜 리스트 조회 테스트 END --')