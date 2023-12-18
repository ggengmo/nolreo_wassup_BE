from django.test import TestCase
from rest_framework.test import APIClient

from account.models import CustomUser as User
from lodging.models import MainLocation, SubLocation, RoomType, Lodging, LodgingReview, LodgingReviewImage

class LodgingReviewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        #user 생성
        signup_data = {
            'email': 'test@test.com',
            'username': 'test',
            'nickname': 'test',
            'password': 'testtest1@2#',
            'password2': 'testtest1@2#',
        }
        login_data = {
            'email': 'test@test.com',
            'password': 'testtest1@2#',
        }
        self.client.post('/account/signup/', signup_data, format='json')
        response = self.client.post('/account/login/', login_data, format='json')
        self.access_token = response.data['access']

        # admin 생성
        User.objects.create_superuser(
            email='testadmin@test.com',
            username='test1',
            nickname='test1',
            password='testtest1@',
        )
        # 로그인
        response = self.client.post(
            '/account/login/',
            {'email': 'testadmin@test.com',
            'password': 'testtest1@'},
            format='json')
        self.admin_access_token = response.data['access']
            

        main_location_data = {
            'address': '테스트 숙소 주소',
        }

        main_location = MainLocation.objects.create(**main_location_data)

        SubLocation.objects.create(
            main_location=main_location, 
            address='테스트 숙소 상세주소'
            )

        # lodging 생성
        data = {
            'name': 'test lodging', 
            'intro': 'test intro', 
            'notice': 'test notice', 
            'info': 'test info', 
            'sub_location': 1, 
        }
        self.client.post('/lodging/', data, HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}', format='json')
        
    def test_lodging_roomtype(self):
        '''
        객실 타입 생성
        '''
        print('객실 타입 생성 테스트 - Begin')
        # 객실 타입 생성 - 비로그인
        data = {
            'name': 'test roomtype',
            'price': 10000,
            'capacity': 2,
            'lodging': 1,
        }
        response = self.client.post(
            '/lodging/roomtype/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 401)

        # 객실 타입 생성 - 로그인
        data = {
            'name': 'test roomtype',
            'price': 10000,
            'capacity': 2,
            'lodging': 1,
        }
        response = self.client.post(
            '/lodging/roomtype/', 
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 201)

        # 객실 타입 생성 - 이름 미입력
        data = {
            'name': '',
            'price': 10000,
            'capacity': 2,
            'lodging': 1,
        }
        response = self.client.post(
            '/lodging/roomtype/', 
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 400)

        # 객실 타입 생성 - 가격 미입력
        data = {
            'name': 'test roomtype',
            'price': '',
            'capacity': 2,
            'lodging': 1,
        }
        response = self.client.post(
            '/lodging/roomtype/', 
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 400)

        # 객실 타입 생성 - 수용 인원 미입력
        data = {
            'name': 'test roomtype',
            'price': 10000,
            'capacity': '',
            'lodging': 1,
        }
        response = self.client.post(
            '/lodging/roomtype/', 
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 400)

        # 객실 타입 생성 - 숙소 미입력
        data = {
            'name': 'test roomtype',
            'price': 10000,
            'capacity': 2,
            'lodging': '',
        }
        response = self.client.post(
            '/lodging/roomtype/', 
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 400)
        print('객실 타입 생성 테스트 - End')

        print('객실 타입 수정 테스트 - Begin')
        # 객실 타입 수정 - 비로그인
        data = {
            'name': 'test roomtype',
            'price': 10000,
            'capacity': 2,
            'lodging': 1,
        }
        response = self.client.patch(
            '/lodging/roomtype/1/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 401)

        # 객실 타입 수정 - 로그인
        data = {
            'name': 'test roomtype',
            'price': 10000,
            'capacity': 2,
            'lodging': 1,
        }
        response = self.client.patch(
            '/lodging/roomtype/1/', 
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 200)

        # 객실 타입 수정 - 없는 객실 타입
        data = {
            'name': 'test roomtype',
            'price': 10000,
            'capacity': 2,
            'lodging': 1,
        }
        response = self.client.patch(
            '/lodging/roomtype/100/', 
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json',
        )
        print('객실 타입 수정 테스트 - End')

        print('객실 타입 삭제 테스트 - Begin')
        # 객실 타입 삭제 - 비로그인
        response = self.client.delete(
            '/lodging/roomtype/1/', 
            format='json',
        )
        self.assertEqual(response.status_code, 401)

        # 객실 타입 삭제 - 로그인
        response = self.client.delete(
            '/lodging/roomtype/1/', 
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 204)

        # 객실 타입 삭제 - 없는 객실 타입
        response = self.client.delete(
            '/lodging/roomtype/100/', 
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 404)

        # 객실 타입 삭제 - 다른 유저
        response = self.client.delete(
            '/lodging/roomtype/1/', 
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 403)
        print('객실 타입 삭제 테스트 - End')

        print('객실 타입 리스트 테스트 - Begin')        
        # 객실 타입 리스트 조회 - 비로그인
        response = self.client.get(
            '/lodging/roomtype/', 
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        print('객실 타입 리스트 테스트 - End')
