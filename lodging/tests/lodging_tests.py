from django.test import TestCase
from rest_framework.test import APIClient

from account.models import CustomUser as User
from lodging.models import MainLocation, SubLocation, Lodging

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

    def test_lodging_create_admin(self):
        '''
        admin 권한 사용자 숙소 생성 테스트
        
        '''
        self.client.force_authenticate(user=self.admin)

        response = self.client.post('/lodging/', self.lodging_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_lodging_create_user(self):
        '''
        user 권한 사용자 숙소 생성 테스트
        '''
        self.client.force_login(user=self.user)
        response = self.client.post('/lodging/', self.lodging_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_lodging_create_no_auth(self):
        '''
        권한 없는 사용자 숙소 생성 테스트
        '''
        response = self.client.post('/lodging/', self.lodging_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_lodging_update_admin(self):
        '''
        admin 권한 사용자 숙소 수정 테스트
        '''
        self.client.force_authenticate(user=self.admin)

        response = self.client.put('/lodging/1/', self.updated_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_lodging_update_user(self): 
        '''
        user 권한 사용자 숙소 수정 테스트
        '''
        self.client.force_login(user=self.user)

        response = self.client.put('/lodging/1/', self.updated_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_lodging_update_no_auth(self):
        '''
        권한 없는 사용자 숙소 수정 테스트
        '''
        response = self.client.put('/lodging/1/', self.updated_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_lodging_list(self):
        '''
        숙소 리스트 테스트
        '''
        response = self.client.get('/lodging/', format='json')
        self.assertEqual(response.status_code, 200)

    def test_lodging_retrieve(self):
        '''
        숙소 조회 테스트
        '''
        response = self.client.get('/lodging/1/', format='json')
        self.assertEqual(response.status_code, 200)