from django.test import TestCase
from rest_framework.test import APIClient

from account.models import CustomUser as User
from lodging.models import MainLocation, SubLocation

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

    def test_lodging_create(self):
        '''
        숙소 생성 테스트
        1. 정상적인 숙소 생성
        '''
        self.client.force_authenticate(user=self.admin)
        main_location_data = {
            'address': '테스트 숙소 주소',
        }
        main_location = MainLocation.objects.create(**main_location_data)

        SubLocation.objects.create(main_location=main_location, address='테스트 숙소 상세주소')

        lodging_data = {
            'name': '테스트 숙소',
            'intro': '테스트 숙소 소개',
            'notice': '테스트 숙소 주의사항',
            'info': '테스트 숙소 정보',
            'price': 100000,
            'sub_location': 1,
        }
        response = self.client.post('/lodging/', lodging_data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 201)
        # self.assertTrue(lodging_data.objects.filter(name='테스트 숙소').exists())