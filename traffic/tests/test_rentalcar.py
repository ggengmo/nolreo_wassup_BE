from django.test import TestCase
from rest_framework.test import APIClient

from account.models import CustomUser as User
from traffic.models import RentalCar, RentalCarImage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.staticfiles import finders

class TestRentalCarCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email = 'test1@gmail.com',
            password = 'testtest1@',
        )
        self.user = User.objects.create_user(
            email = 'test2@gmail.com',
            password = 'testtest2@',
            nickname = 'test2',
        )
        # # 렌트카 데이터 생성
        # for i in range(10):
        #     RentalCar.objects.create(
        #         model = '소나타',
        #         area = '서울',
        #         num = f'{12341 + i}',
        #         price = '10000',
        #     )

    def test_RentalCar_create_admin(self):
        '''
        렌트카 생성 테스트(관리자)
        '''
        print('-- 렌트카 생성 테스트(관리자) BEGIN --')
        # 정상 처리 테스트
        self.client.force_authenticate(user=self.admin)
        RentalCar_data = {
            'model': '소나타',
            'area': '서울',
            'num': '99599',
            'price': '10000',
        }
        response = self.client.post('/traffic/rentalcar/', RentalCar_data, format='json')
        self.assertEqual(response.status_code, 201)

        # 비정상 처리 테스트 - 차량 번호가 중복일 경우
        RentalCar_data = {
            'model': '소나타',
            'area': '서울',
            'num': '99599',
            'price': '10000',
        }
        response = self.client.post('/traffic/rentalcar/', RentalCar_data, format='json')
        self.assertEqual(response.status_code, 400)
        # 비정상 처리 테스트 - 차량 모델이 없을 경우
        RentalCar_data = {
            'model': '',
            'area': '서울',
            'num': '99919',
            'price': '10000',
        }
        response = self.client.post('/traffic/rentalcar/', RentalCar_data, format='json')
        self.assertEqual(response.status_code, 400)
        # 비정상 처리 테스트 - 차량 지역이 없을 경우
        RentalCar_data = {
            'model': '소나타',
            'area': '',
            'num': '99929',
            'price': '10000',
        }
        response = self.client.post('/traffic/rentalcar/', RentalCar_data, format='json')
        self.assertEqual(response.status_code, 400)
        # 비정상 처리 테스트 - 차량 번호가 없을 경우
        RentalCar_data = {
            'model': '소나타',
            'area': '서울',
            'num': '',
            'price': '10000',
        }
        response = self.client.post('/traffic/rentalcar/', RentalCar_data, format='json')
        self.assertEqual(response.status_code, 400)
        # 비정상 처리 테스트 - 차량 가격이 없을 경우
        RentalCar_data = {
            'model': '소나타',
            'area': '서울',
            'num': '99939',
            'price': '',
        }
        response = self.client.post('/traffic/rentalcar/', RentalCar_data, format='json')
        self.assertEqual(response.status_code, 400)
        print('-- 렌트카 생성 테스트(관리자) END --')

    def test_RentalCar_create_user(self):
        '''
        렌트카 생성 테스트(유저)
        '''
        print('-- 렌트카 생성 테스트(유저) BEGIN --')
        # 정상 처리 테스트
        self.client.force_login(user=self.user)
        RentalCar_data = {
            'model': '소나타',
            'area': '서울',
            'num': '99599',
            'price': '10000',
        }
        response = self.client.post('/traffic/rentalcar/', RentalCar_data, format='json')
        self.assertEqual(response.status_code, 401)
        print('-- 렌트카 생성 테스트(유저) END --')

    def test_RentalCar_list(self):
        '''
        렌트카 리스트 테스트
        '''
        print('-- 렌트카 리스트 테스트 BEGIN --')
        # 정상 처리 테스트
        response = self.client.get('/traffic/rentalcar/')
        self.assertEqual(response.status_code, 200)
        print('-- 렌트카 리스트 테스트 END --')

    def test_RentalCar_retrieve(self):
        '''
        렌트카 조회 테스트
        '''
        print('-- 렌트카 조회 테스트 BEGIN --')
        # 정상 처리 테스트
        response = self.client.get('/traffic/rentalcar/1/')
        self.assertEqual(response.status_code, 200)
        # 비정상 처리 테스트 - 존재하지 않는 렌트카 조회 시도
        response = self.client.get('/traffic/rentalcar/100/')
        self.assertEqual(response.status_code, 404)
        print('-- 렌트카 조회 테스트 END --')

    def test_RentalCar_update_admin(self):
        '''
        렌트카 수정 테스트(관리자)
        '''
        print('-- 렌트카 수정 테스트(관리자) BEGIN --')
        # 정상 처리 테스트
        self.client.force_authenticate(user=self.admin)
        RentalCar_data = {
            'model': '소나타',
            'area': '서울',
            'num': '99599',
            'price': '10000',
        }
        response = self.client.put('/traffic/rentalcar/1/', RentalCar_data, format='json')
        self.assertEqual(response.status_code, 200)
        # 비정상 처리 테스트 - 존재하지 않는 렌트카 수정 시도
        RentalCar_data = {
            'model': '소나타',
            'area': '서울',
            'num': '99599',
            'price': '10000',
        }
        response = self.client.put('/traffic/rentalcar/100/', RentalCar_data, format='json')
        self.assertEqual(response.status_code, 404)
        # 비정상 처리 테스트 - 차량 번호가 중복일 경우
        RentalCar_data = {
            'model': '소나타',
            'area': '서울',
            'num': '12345',
            'price': '10000',
        }
        response = self.client.put('/traffic/rentalcar/1/', RentalCar_data, format='json')
        self.assertEqual(response.status_code, 400)
        # 비정상 처리 테스트 - 차량 모델이 없을 경우
        RentalCar_data = {
            'model': '',
            'area': '서울',
            'num': '99919',
            'price': '10000',
        }
        response = self.client.put('/traffic/rentalcar/1/', RentalCar_data, format='json')
        self.assertEqual(response.status_code, 400)
        # 비정상 처리 테스트 - 차량 지역이 없을 경우
        RentalCar_data = {
            'model': '소나타',
            'area': '',
            'num': '99929',
            'price': '10000',
        }
        response = self.client.put('/traffic/rentalcar/1/', RentalCar_data, format='json')
        self.assertEqual(response.status_code, 400)
        print('-- 렌트카 수정 테스트(관리자) END --')

    def test_RentalCar_update_user(self):
        '''
        렌트카 수정 테스트(유저)
        '''
        print('-- 렌트카 수정 테스트(유저) BEGIN --')
        # 정상 처리 테스트
        self.client.force_login(user=self.user)
        RentalCar_data = {
            'model': '소나타',
            'area': '서울',
            'num': '99599',
            'price': '10000',
        }
        response = self.client.put('/traffic/rentalcar/1/', RentalCar_data, format='json')
        self.assertEqual(response.status_code, 401)
        print('-- 렌트카 수정 테스트(유저) END --')

    def test_RentalCar_destroy_admin(self):
        '''
        렌트카 삭제 테스트(관리자)
        '''
        print('-- 렌트카 삭제 테스트(관리자) BEGIN --')
        # 정상 처리 테스트
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete('/traffic/rentalcar/1/')
        self.assertEqual(response.status_code, 204)
        # 비정상 처리 테스트 - 존재하지 않는 렌트카 삭제 시도
        response = self.client.delete('/traffic/rentalcar/100/')
        self.assertEqual(response.status_code, 404)
        print('-- 렌트카 삭제 테스트(관리자) END --')

    def test_RentalCar_destroy_user(self):
        '''
        렌트카 삭제 테스트(유저)
        '''
        print('-- 렌트카 삭제 테스트(유저) BEGIN --')
        # 비정상 처리 테스트 - 유저가 렌트카 삭제 시도
        self.client.force_login(user=self.user)
        response = self.client.delete('/traffic/rentalcar/1/')
        self.assertEqual(response.status_code, 401)
        print('-- 렌트카 삭제 테스트(유저) END --')

    def test_RentalCarImage_create_admin(self):
        '''
        렌트카 이미지 생성 테스트(관리자)
        '''
        print('-- 렌트카 이미지 생성 테스트(관리자) BEGIN --')
        # 정상 처리 테스트
        self.client.force_authenticate(user=self.admin)
        images = []
        for i in range(3):
            images.append(SimpleUploadedFile(name=f'test_image{i}.jpg', 
            content=open('static/assets/images/test_image/ormi.jpg', 'rb').read(), 
            content_type='image/jpeg'))
        RentalCar_data = {
            'model': '소나타',
            'area': '서울',
            'num': '99599',
            'price': '10000',
            'image': images,
        }
        response = self.client.post('/traffic/rentalcar/', RentalCar_data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(RentalCarImage.objects.all().count(), 3)
        self.assertEqual(RentalCarImage.objects.all()[0].rental_car.pk, 1)
        self.assertEqual(RentalCar.objects.all()[0].rental_car_images.count(), 3)
        print('-- 렌트카 이미지 생성 테스트(관리자) END --')
    
    def test_RentalCarImage_create_user(self):
        '''
        렌트카 이미지 생성 테스트(유저)
        '''
        print('-- 렌트카 이미지 생성 테스트(유저) BEGIN --')
        # 비정상 처리 테스트 - 유저가 렌트카 이미지 생성 시도
        self.client.force_login(user=self.user)
        images = []
        for i in range(3):
            images.append(SimpleUploadedFile(name=f'test_image{i}.jpg', 
            content=open('static/assets/images/test_image/ormi.jpg', 'rb').read(), 
            content_type='image/jpeg'))
        RentalCar_data = {
            'model': '소나타',
            'area': '서울',
            'num': '99599',
            'price': '10000',
            'image': images,
        }
        response = self.client.post('/traffic/rentalcar/', RentalCar_data, format='multipart')
        self.assertEqual(response.status_code, 401)
        print('-- 렌트카 이미지 생성 테스트(관리자) END --')