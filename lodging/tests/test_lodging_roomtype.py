from django.test import TestCase
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

from account.models import CustomUser as User
from lodging.models import MainLocation, SubLocation, RoomType
from utils.tools import remove_media_folder

class LodgingRoomtypeTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.image = SimpleUploadedFile(name='test_image.jpg', 
        content=open('static/assets/images/test_image/ormi.jpg', 'rb').read(), 
        content_type='image/jpeg')

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

        data = {
            'name': 'test roomtype',
            'price': 10000,
            'capacity': 2,
            'lodging': 1,
        }
        self.client.post(
            '/lodging/roomtype/', 
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json',
        )
        
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

        print('객실 타입 이미지 생성 테스트 - Begin')
        # 객실 타입 이미지 생성 - 비로그인
        data = {
            'image': self.image,
            'is_main': False,
            'room_type': 1,
        }
        response = self.client.post(
            '/lodging/roomtype/image/', 
            data,
            format='multipart',
        )
        self.assertEqual(response.status_code, 401)

        # 객실 타입 이미지 생성 - 권한 없는 유저
        data = {
            'image': self.image,
            'is_main': True,
            'room_type': 1,
        }
        response = self.client.post(
            '/lodging/roomtype/image/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='multipart',
        )
        self.assertEqual(response.status_code, 403)

        # 객실 타입 이미지 생성 - 권한 있는 유저
        image = SimpleUploadedFile(name='test_image.jpg', 
        content=open('static/assets/images/test_image/ormi.jpg', 'rb').read(), 
        content_type='image/jpeg')
        
        data = {
            'image': image,
            'is_main': True,
            'room_type': 2,
        }
        response = self.client.post(
            '/lodging/roomtype/image/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='multipart',
        )
        self.assertEqual(response.status_code, 201)

        # 객실 타입 이미지 생성 - 이미지 미입력
        data = {
            'image': '',
            'is_main': True,
            'room_type': 2,
        }
        response = self.client.post(
            '/lodging/roomtype/image/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='multipart',
        )
        self.assertEqual(response.status_code, 400)

        # 객실 타입 이미지 생성 - 메인 이미지 중복 등록
        data = {
            'image': image,
            'is_main': True,
            'room_type': 2,
        }
        response = self.client.post(
            '/lodging/roomtype/image/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='multipart',
        )
        self.assertEqual(response.status_code, 400)

        # 객실 타입 이미지 생성 - 등록되지 않은 객실 타입
        data = {
            'image': image,
            'is_main': False,
            'room_type': 100,
        }
        response = self.client.post(
            '/lodging/roomtype/image/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='multipart',
        )
        self.assertEqual(response.status_code, 400)
        print('객실 타입 이미지 생성 테스트 - End')

        print('객실 타입 이미지 수정 테스트 - Begin')
        # 객실 타입 이미지 수정 - 비로그인
        data = {
            'image': image,
            'is_main': False,
            'room_type': 2,
        }
        response = self.client.patch(
            '/lodging/roomtype/image/1/',
            data,
            format='multipart',
        )
        self.assertEqual(response.status_code, 401)

        # 객실 타입 이미지 수정 - 권한 없는 유저
        data = {
            'image': image,
            'is_main': False,
            'room_type': 2,
        }
        response = self.client.patch(
            '/lodging/roomtype/image/1/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='multipart',
        )
        self.assertEqual(response.status_code, 403)

        # 객실 타입 이미지 수정 - 권한 있는 유저
        image = SimpleUploadedFile(name='test_image.jpg', 
        content=open('static/assets/images/test_image/ormi.jpg', 'rb').read(), 
        content_type='image/jpeg')

        data = {
            'image': image,
            'is_main': False,
            'room_type': 2,
        }
        response = self.client.patch(
            '/lodging/roomtype/image/1/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='multipart',
        )
        self.assertEqual(response.status_code, 200)
        print('객실 타입 이미지 수정 테스트 - End')

        print('객실 타입 이미지 삭제 테스트 - Begin')
        # 객실 타입 이미지 삭제 - 비로그인
        response = self.client.delete(
            '/lodging/roomtype/image/1/',
            format='multipart',
        )
        self.assertEqual(response.status_code, 401)

        # 객실 타입 이미지 삭제 - 권한 없는 유저
        response = self.client.delete(
            '/lodging/roomtype/image/1/',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='multipart',
        )
        self.assertEqual(response.status_code, 403)

        # 객실 타입 이미지 삭제 - 권한 있는 유저
        response = self.client.delete(
            '/lodging/roomtype/image/1/',
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='multipart',
        )
        self.assertEqual(response.status_code, 204)

        # 객실 타입 이미지 삭제 - 없는 이미지
        response = self.client.delete(
            '/lodging/roomtype/image/100/',
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='multipart',
        )
        self.assertEqual(response.status_code, 404)
        print('객실 타입 이미지 삭제 테스트 - End')

        print('객실 타입 이미지 리스트 테스트 - Begin')
        # 객실 타입 이미지 리스트
        response = self.client.get(
            '/lodging/roomtype/image/',
            format='multipart',
        )
        self.assertEqual(response.status_code, 200)
        print('객실 타입 이미지 리스트 테스트 - End')

        # 테스트 종료 후 media 폴더 삭제
        remove_media_folder()
        return super().tearDown()