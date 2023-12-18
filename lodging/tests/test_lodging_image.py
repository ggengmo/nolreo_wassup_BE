import os

from pathlib import Path
from django.test import TestCase
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

from account.models import CustomUser as User
from lodging.models import MainLocation, SubLocation, Lodging, LodgingImage
from utils.tools import remove_media_folder
class LodgingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            nickname='testuser',
            password='testpassword'
            )

        self.admin = User.objects.create_superuser(
            email='admin@example.com',  
            password='admin1@2#3$4'
            )

        self.client = APIClient()

        # test data
        main_location_data = {
            'address': '테스트 숙소 주소',
        }

        main_location = MainLocation.objects.create(**main_location_data)

        SubLocation.objects.create(
            main_location=main_location, 
            address='테스트 숙소 상세주소'
            )
        
        image = SimpleUploadedFile(name='test_image.jpg', 
                                content=open('static/assets/images/test_image/ormi.jpg', 'rb').read(), 
                                content_type='image/jpeg')
        
        Lodging.objects.create(
            name='테스트 숙소',
            intro='테스트 숙소 소개',
            notice='테스트 숙소 주의사항',
            info='테스트 숙소 정보',
            sub_location=SubLocation.objects.get(id=1),
        )

        LodgingImage.objects.create(
            image=image,
            is_main=True,
            lodging=Lodging.objects.get(id=1),
        )
        self.lodging_image = LodgingImage.objects.get(id=1)

        self.lodging_data = {  
            'name': '테스트 숙소',
            'intro': '테스트 숙소 소개',
            'notice': '테스트 숙소 주의사항',
            'info': '테스트 숙소 정보',
            'sub_location': 1,
            'lodging_images': LodgingImage.objects.get(id=1),
        }

    def test_lodging_create_admin(self):
        '''
        이미지 포함 사용자 숙소 생성 테스트
        '''
        print('-- 이미지 포함 사용자 숙소 생성 테스트 END --')
        self.client.force_authenticate(user=self.admin)

        response = self.client.post('/lodging/', self.lodging_data, format='multipart')
        self.assertEqual(response.status_code, 201)
        print('-- 이미지 포함 사용자 숙소 생성 테스트 END --')

    def test_lodging_image_update(self):
        '''
        숙소 이미지 수정 테스트
        '''
        print('-- 숙소 이미지 수정 테스트 END --')
        self.client.force_authenticate(user=self.admin)

        image = SimpleUploadedFile(name='test_image.jpg', 
                                content=open('static/assets/images/test_image/ormi.jpg', 'rb').read(), 
                                content_type='image/jpeg')
        
        lodging_image_data = {
            'image': image,
            'is_main': False,
            'lodging': 1,
        }

        response = self.client.put('/lodging/images/1/', lodging_image_data)
        self.assertEqual(response.status_code, 200)

        '''
        숙소 이미지 수정 테스트 - 메인 이미지 중복 등록
        '''
        lodging_image_data = {
            'image': image,
            'is_main': True,
            'lodging': 1,
        }

        response = self.client.put('/lodging/images/1/', lodging_image_data)
        self.assertEqual(response.status_code, 400)

        '''
        숙소 이미지 수정 테스트 - 등록되지 않은 숙소
        '''
        lodging_image_data = {
            'image': image,
            'is_main': False,
            'lodging': 2,
        }

        response = self.client.put('/lodging/images/1/', lodging_image_data)
        self.assertEqual(response.status_code, 400)
        print('-- 숙소 이미지 수정 테스트 END --')

    def test_lodging_image_delete(self):
        '''
        숙소 이미지 삭제 테스트
        '''
        print('-- 숙소 이미지 삭제 테스트 END --')
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete('/lodging/images/1/')
        self.assertEqual(response.status_code, 204)

        '''
        숙소 이미지 삭제 테스트 - 등록되지 않은 이미지
        '''
        response = self.client.delete('/lodging/images/2/')
        self.assertEqual(response.status_code, 404)
        print('-- 숙소 이미지 삭제 테스트 END --')
    
    def test_lodging_image_retrieve(self):
        '''
        숙소 이미지 조회 테스트
        '''
        print('-- 숙소 이미지 조회 테스트 BEGIN --')
        response = self.client.get('/lodging/images/1/')
        self.assertEqual(response.status_code, 200)

        '''
        숙소 이미지 조회 테스트 - 등록되지 않은 이미지
        '''
        response = self.client.get('/lodging/images/2/')
        self.assertEqual(response.status_code, 404)
        print('-- 숙소 이미지 조회 테스트 END --')

    def tearDown(self):
        remove_media_folder()
        return super().tearDown()