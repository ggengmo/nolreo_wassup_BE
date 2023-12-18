from django.test import TestCase
from rest_framework.test import APIClient

from account.models import CustomUser as User
from lodging.models import MainLocation, SubLocation, Lodging, LodgingReview, LodgingReviewImage
from django.core.files.uploadedfile import SimpleUploadedFile

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
        
        # lodging review 생성
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
    
    def test_create_lodging_review_comment(self):
        '''
        숙소 리뷰 댓글 생성 테스트
        '''
        print('숙소 리뷰 댓글 생성 테스트 - Begin')
        
        # 숙소 리뷰 댓글 생성 테스트 - 인증X
        data = {
            'content': 'test content',
            'lodging_review': 1,
            'user': 1,
        }

        response = self.client.post(
            '/lodging/review/1/comment/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 401)

        #숙소 리뷰 댓글 생성 테스트 - 인증O
        data = {
            'content': 'test content',
            'lodging_review': 1,
            'user': 1,
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(
            '/lodging/review/1/comment/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 201)

        #숙소 리뷰 댓글 생성 테스트 - 숙소 리뷰 없음
        data = {
            'content': 'test content',
            'lodging_review': 100,
            'user': 1,
        }
        response = self.client.post(
            '/lodging/review/100/comment/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 400)

        #숙소 리뷰 댓글 생성 테스트 - 유저 없음
        data = {
            'content': 'test content',
            'lodging_review': 1,
            'user': 100,
        }
        response = self.client.post(
            '/lodging/review/1/comment/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 400)
        print('숙소 리뷰 댓글 생성 테스트 - End')

        print('숙소 리뷰 댓글 수정 테스트 - Begin')
        # 숙소 리뷰 댓글 수정 테스트 - 인증O
        data = {
            'content': 'test content',
            'lodging_review': 1,
            'user': 1,
        }
        response = self.client.patch(
            '/lodging/review/1/comment/1/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 200)

        #숙소 리뷰 댓글 수정 테스트 - 숙소 리뷰 없음
        data = {
            'content': 'test content',
            'lodging_review': 100,
            'user': 1,
        }
        response = self.client.patch(
            '/lodging/review/100/comment/1/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 400)

        #숙소 리뷰 댓글 수정 테스트 - 유저 없음
        data = {
            'content': 'test content',
            'lodging_review': 1,
            'user': 100,
        }
        response = self.client.patch(
            '/lodging/review/1/comment/1/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 400)

        #숙소 리뷰 댓글 수정 테스트 - 댓글 없음
        data = {
            'content': 'test content',
            'lodging_review': 1,
            'user': 1,
        }
        response = self.client.patch(
            '/lodging/review/1/comment/100/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 404)
        print('숙소 리뷰 댓글 수정 테스트 - End')

        print('숙소 리뷰 댓글 리스트 테스트 - Begin')
        #숙소 리뷰 댓글 리스트 테스트 - 인증O
        data = {
            'content': 'test content',
            'lodging_review': 1,
            'user': 1,
        }
        response = self.client.get(
            '/lodging/review/1/comment/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        print('숙소 리뷰 댓글 리스트 테스트 - End')

        print('숙소 리뷰 댓글 삭제 테스트 - Begin')
        #숙소 리뷰 댓글 삭제 테스트 - 인증O
        response = self.client.delete(
            '/lodging/review/1/comment/1/', 
            format='json',
        )
        self.assertEqual(response.status_code, 204)
        print('숙소 리뷰 댓글 삭제 테스트 - End')