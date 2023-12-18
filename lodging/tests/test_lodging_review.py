from .test_setup import LogingTestCase

from django.core.files.uploadedfile import SimpleUploadedFile
from utils.tools import remove_media_folder

class LodgingReviewTest(LogingTestCase):
    def setUp(self):
        super().setUp()

    def test_lodging_review(self):
        '''
        숙소 리뷰 CRUD 테스트
        '''
        print('숙소 리뷰 생성 테스트 - Begin')
        
        # 숙소 리뷰 생성 테스트 - 로그인X
        data = {
            'title': 'test title',
            'content': 'test content',
            'star_score': 5,
            'lodging': 1,
            'user': 1,
        }
        response = self.client.post(
            '/lodging/review/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 401)

        #숙소 리뷰 생성 테스트 - 로그인O
        data = {
            'title': 'test title',
            'content': 'test content',
            'star_score': 5,
            'lodging': 1,
            'user': 1,
        }

        response = self.client.post(
            '/lodging/review/', 
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 201)

        #숙소 리뷰 생성 테스트 - 숙소 없음
        data = {
            'title': 'test title',
            'content': 'test content',
            'star_score': 5,
            'lodging': 100,
            'user': 1,
        }
        response = self.client.post(
            '/lodging/review/', 
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 400)

        #숙소 리뷰 생성 테스트 - 유저 없음
        data = {
            'title': 'test title',
            'content': 'test content',
            'star_score': 5,
            'lodging': 1,
            'user': 100,
        }
        response = self.client.post(
            '/lodging/review/', 
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 400)

        #숙소 리뷰 생성 테스트 - 별점 없음
        data = {
            'title': 'test title',
            'content': 'test content',
            'star_score': None,
            'lodging': 1,
            'user': 1,
        }
        response = self.client.post(
            '/lodging/review/', 
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 400)

        #숙소 리뷰 생성 테스트 - 별점 범위 초과
        data = {
            'title': 'test title',
            'content': 'test content',
            'star_score': 6,
            'lodging': 1,
            'user': 1,
        }
        response = self.client.post(
            '/lodging/review/', 
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 400)

        #숙소 리뷰 생성 테스트 - 내용 없음
        data = {
            'title': 'test title',
            'content': None,
            'star_score': 5,
            'lodging': 1,
            'user': 1,
        }
        response = self.client.post(
            '/lodging/review/', 
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 400)
        print('숙소 리뷰 생성 테스트 - End')

        print('숙소 리뷰 수정 테스트 - Begin')
        #숙소 리뷰 수정 테스트
        data = {
            'title': 'test title',
            'content': 'test content',
            'star_score': 4,
            'lodging': 1,
            'user': 1,
        }

        response = self.client.patch(
            '/lodging/review/1/', 
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        print('숙소 리뷰 수정 테스트 - End')

        print('숙소 리뷰 리스트 테스트 - Begin')
        #숙소 리뷰 리스트 테스트
        response = self.client.get(
            '/lodging/review/', 
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        print('숙소 리뷰 리스트 테스트 - End')

        print('숙소 리뷰 이미지 생성 테스트 - Begin')
        #숙소 리뷰 이미지 생성 테스트
        image = SimpleUploadedFile(name='test_image.jpg', 
                                content=open('static/assets/images/test_image/ormi.jpg', 'rb').read(), 
                                content_type='image/jpeg')

        data = {
            'image': image,
            'lodging_review': 1,
        }

        response = self.client.post(
            '/lodging/review/image/', 
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='multipart',
        )
        self.assertEqual(response.status_code, 201)

        #숙소 리뷰 이미지 생성 테스트 - 리뷰 없음
        data = {
            'image': 'test image',
            'lodging_review': 100,
        }
        response = self.client.post(
            '/lodging/review/image/', 
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 400)

        #숙소 리뷰 이미지 생성 테스트 - 이미지 없음
        data = {
            'image': None,
            'lodging_review': 1,
        }
        response = self.client.post(
            '/lodging/review/image/', 
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 400)
        print('숙소 리뷰 이미지 생성 테스트 - End')

        print('숙소 리뷰 이미지 수정 테스트 - Begin')
        #숙소 리뷰 이미지 수정 테스트 
        image = SimpleUploadedFile(name='test_image.jpg', 
                        content=open('static/assets/images/test_image/ormi.jpg', 'rb').read(), 
                        content_type='image/jpeg')
        data = {
            'image': image,
            'lodging_review': 1,
        }
        response = self.client.patch(
            '/lodging/review/image/1/',
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='multipart',
        )
        self.assertEqual(response.status_code, 200)

        #숙소 리뷰 이미지 수정 테스트 - 리뷰 없음
        data = {
            'image': image,
            'lodging_review': 100,
        }
        response = self.client.patch(
            '/lodging/review/image/1/',
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='multipart',
        )
        self.assertEqual(response.status_code, 400)
        print('숙소 리뷰 이미지 수정 테스트 - End')

        print('숙소 리뷰 삭제 테스트 - Begin')
        #숙소 리뷰 삭제 테스트
        response = self.client.delete(
            '/lodging/review/1/', 
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 204)

        #숙소 리뷰 삭제 테스트 - 없는 리뷰
        response = self.client.delete(
            '/lodging/review/100/', 
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json',
        )
        self.assertEqual(response.status_code, 404)

        #숙소 리뷰 삭제 테스트 - 로그인X
        response = self.client.delete(
            '/lodging/review/1/', 
            format='json',
        )
        self.assertEqual(response.status_code, 401)
        print('숙소 리뷰 삭제 테스트 - End')

        # 테스트 종료 후 media 폴더 삭제
        remove_media_folder()
        return super().tearDown()