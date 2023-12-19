from django.test import TestCase
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

from account.models import CustomUser as User
from lodging.models import MainLocation, SubLocation, Lodging, LodgingImage

class LogingTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.image = SimpleUploadedFile(name='test_image.jpg', 
        content=open('static/assets/images/test_image/ormi.jpg', 'rb').read(), 
        content_type='image/jpeg')

        #user 생성 및 로그인
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

        # admin 생성 및 로그인
        User.objects.create_superuser(
            email='testadmin@test.com',
            username='test1',
            nickname='test1',
            password='testtest1@',
        )
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
        return super().setUp()
    
    def setUp_lodging(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email='testuser@example.com',
            nickname='testuser',
            password='testpassword'
            )

        self.admin = User.objects.create_superuser(
            email='admin@example.com',  
            password='admin1@2#3$4'
            )

        # test data
        main_location_data = {
            'address': '테스트 숙소 주소',
        }

        main_location = MainLocation.objects.create(**main_location_data)

        SubLocation.objects.create(
            main_location=main_location, 
            address='테스트 숙소 상세주소'
            )

        Lodging.objects.create(
            name='테스트 숙소',
            intro='테스트 숙소 소개',
            notice='테스트 숙소 주의사항',
            info='테스트 숙소 정보',
            sub_location=SubLocation.objects.get(id=1),
        )
        
        self.lodging_data = {  
            'name': '테스트 숙소',
            'intro': '테스트 숙소 소개',
            'notice': '테스트 숙소 주의사항',
            'info': '테스트 숙소 정보',
            'sub_location': 1,
        }

        self.updated_data = {
        'name': '수정된 테스트 숙소',
        'intro': '수정된 테스트 숙소 소개',
        'notice': '수정된 테스트 숙소 주의사항',
        'info': '수정된 테스트 숙소 정보',
        'sub_location': 1,
    }
    
    def setUp_lodging_image(self):
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

    def setUp_lodging_comment(self):
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

    def setUp_location(self):
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

        # main_location 생성
        data = {
            'address': '서울시 송파구 방이동',
        }
        self.client.post('/lodging/mainlocation/', data, HTTP_AUTHORIZATION=f'Bearer {self.access_token}', format='json')