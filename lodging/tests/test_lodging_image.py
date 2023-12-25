from .test_setup import LogingTestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from utils.test_remove_tools import remove_media_folder
class LodgingImageTestCase(LogingTestCase):
    def setUp(self):
        super().setUp_lodging_image()

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

        response = self.client.patch('/lodging/images/1/', lodging_image_data)
        self.assertEqual(response.status_code, 200)

        '''
        숙소 이미지 수정 테스트 - 메인 이미지 중복 등록
        '''
        lodging_image_data = {
            'image': image,
            'is_main': True,
            'lodging': 1,
        }

        response = self.client.patch('/lodging/images/1/', lodging_image_data)
        self.assertEqual(response.status_code, 400)

        '''
        숙소 이미지 수정 테스트 - 등록되지 않은 숙소
        '''
        lodging_image_data = {
            'image': image,
            'is_main': False,
            'lodging': 2,
        }

        response = self.client.patch('/lodging/images/1/', lodging_image_data)
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

    # 테스트 종료 후 media 폴더 삭제
        remove_media_folder()
        return super().tearDown()