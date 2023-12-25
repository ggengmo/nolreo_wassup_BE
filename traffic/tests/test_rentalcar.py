from django.test import TestCase
from rest_framework.test import APIClient

from account.models import CustomUser as User
from traffic.models import RentalCar, RentalCarImage, RentalCarReview, RentalCarReviewComment, RentalCarReviewImage
from django.core.files.uploadedfile import SimpleUploadedFile
from utils.test_remove_tools import remove_media_folder


class TestRentalCarCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # 렌트카 데이터 생성
        for i in range(10):
            RentalCar.objects.create(
                model = '소나타',
                area = '서울',
                num = f'{12341 + i}',
                price = '10000',
            )
        user = self.user()
        for i in range(10):
            RentalCarReview.objects.create(
                title = f'렌트카 리뷰 제목 {i}',
                content = f'렌트카 리뷰 내용 {i}',
                star_score = '5',
                rental_car = RentalCar.objects.get(pk=1),
                user = user,
            )
        for i in range(10):
            RentalCarReviewComment.objects.create(
                content = f'렌트카 리뷰 댓글 내용 {i}',
                rental_car_review = RentalCarReview.objects.get(pk=1),
                user = user,
            )

    def admin(self):
        '''
        관리자 생성
        '''
        user = User.objects.create_superuser(
            email='test@gmail.com',
            username='test',
            nickname='test',
            password='testtest1@',
        )
        # 로그인
        response = self.client.post(
            '/account/login/',
            {'email': 'test@gmail.com',
            'password': 'testtest1@'},
            format='json')
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        user.save()
        return user
    
    def user(self):
        '''
        사용자 생성
        '''
        user = User.objects.create_user(
            email='test1@gmail.com',
            username='test1',
            nickname='test2',
            password='testtest1@',
        )
        # 로그인
        response = self.client.post(
            '/account/login/',
            {'email': 'test1@gmail.com',
            'password': 'testtest1@'},
            format='json')
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        user.save()
        return user

    def test_RentalCar_create_admin(self):
        '''
        렌트카 생성 테스트(관리자)
        '''
        print('-- 렌트카 생성 테스트(관리자) BEGIN --')
        # 정상 처리 테스트
        self.admin()
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
        렌트카 생성 테스트(일반 사용자)
        '''
        print('-- 렌트카 생성 테스트(일반 사용자) BEGIN --')
        # 정상 처리 테스트
        RentalCar_data = {
            'model': '소나타',
            'area': '서울',
            'num': '99599',
            'price': '10000',
        }
        response = self.client.post('/traffic/rentalcar/', RentalCar_data, format='json')
        self.assertEqual(response.status_code, 403)
        print('-- 렌트카 생성 테스트(일반 사용자) END --')

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
        self.admin()
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
        렌트카 수정 테스트(일반 사용자)
        '''
        print('-- 렌트카 수정 테스트(일반 사용자) BEGIN --')
        # 비정상 처리 테스트
        RentalCar_data = {
            'model': '소나타',
            'area': '서울',
            'num': '99599',
            'price': '10000',
            'user': 1,
        }
        response = self.client.put('/traffic/rentalcar/1/', RentalCar_data, format='json')
        self.assertEqual(response.status_code, 403)
        print('-- 렌트카 수정 테스트(일반 사용자) END --')

    def test_RentalCar_destroy_admin(self):
        '''
        렌트카 삭제 테스트(관리자)
        '''
        print('-- 렌트카 삭제 테스트(관리자) BEGIN --')
        # 정상 처리 테스트
        self.admin()
        response = self.client.delete('/traffic/rentalcar/1/')
        self.assertEqual(response.status_code, 204)
        # 비정상 처리 테스트 - 존재하지 않는 렌트카 삭제 시도
        response = self.client.delete('/traffic/rentalcar/100/')
        self.assertEqual(response.status_code, 404)
        print('-- 렌트카 삭제 테스트(관리자) END --')

    def test_RentalCar_destroy_user(self):
        '''
        렌트카 삭제 테스트(일반 사용자)
        '''
        print('-- 렌트카 삭제 테스트(일반 사용자) BEGIN --')
        # 비정상 처리 테스트 - 일반 사용자가 렌트카 삭제 시도
        response = self.client.delete('/traffic/rentalcar/1/')
        self.assertEqual(response.status_code, 403)
        print('-- 렌트카 삭제 테스트(일반 사용자) END --')

    def test_RentalCarImage_create_admin(self):
        '''
        렌트카 이미지 생성 테스트(관리자)
        '''
        print('-- 렌트카 이미지 생성 테스트(관리자) BEGIN --')
        # 정상 처리 테스트
        self.admin()
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
        self.assertEqual(RentalCarImage.objects.all()[0].rental_car.pk, 11)
        self.assertEqual(RentalCar.objects.all()[10].rental_car_images.count(), 3)
        remove_media_folder()
        print('-- 렌트카 이미지 생성 테스트(관리자) END --')
    
    def test_RentalCarImage_create_user(self):
        '''
        렌트카 이미지 생성 테스트(일반 사용자)
        '''
        print('-- 렌트카 이미지 생성 테스트(일반 사용자) BEGIN --')
        # 비정상 처리 테스트 - 일반 사용자가 렌트카 이미지 생성 시도
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
        self.assertEqual(response.status_code, 403)
        print('-- 렌트카 이미지 생성 테스트(일반 사용자) END --')

    def test_RentalCarImage_destroy_admin(self):
        '''
        렌트카 이미지 삭제 테스트(관리자)
        '''
        print('-- 렌트카 이미지 삭제 테스트(관리자) BEGIN --')
        # 정상 처리 테스트
        self.admin()
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
        self.assertEqual(RentalCarImage.objects.all()[0].rental_car.pk, 11)
        self.assertEqual(RentalCar.objects.all()[10].rental_car_images.count(), 3)
        response = self.client.delete('/traffic/rentalcar/image/1/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(RentalCarImage.objects.all().count(), 2)
        response = self.client.delete('/traffic/rentalcar/image/2/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(RentalCar.objects.all()[10].rental_car_images.count(), 1)
        # 비정상 처리 테스트 - 존재하지 않는 렌트카 이미지 삭제 시도
        response = self.client.delete('/traffic/rentalcar/image/100/')
        self.assertEqual(response.status_code, 404)
        remove_media_folder()
        print('-- 렌트카 이미지 삭제 테스트(관리자) END --')

    def test_RentalCarImage_destroy_user(self):
        '''
        렌트카 이미지 삭제 테스트(일반 사용자)
        '''
        print('-- 렌트카 이미지 삭제 테스트(일반 사용자) BEGIN --')
        # 비정상 처리 테스트 - 일반 사용자가 렌트카 이미지 삭제 시도
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
            'user': 1,
            'image': images,
        }
        response = self.client.post('/traffic/rentalcar/', RentalCar_data, format='multipart')
        response = self.client.delete('/traffic/rentalcar/image/1/')
        self.assertEqual(response.status_code, 403)
        print('-- 렌트카 이미지 삭제 테스트(일반 사용자) END --')

    def test_RentalCarReview_create_user(self):
        '''
        렌트카 리뷰 생성 테스트(일반 사용자)
        '''
        print('-- 렌트카 리뷰 생성 테스트(일반 사용자) BEGIN --')
        # 정상 처리 테스트
        RentalCarReview_data = {
            'title': '렌트카 리뷰 제목',
            'content': '렌트카 리뷰 내용',
            'star_score': '5',
            'rental_car': 1,
            'user': 1,
        }
        response = self.client.post('/traffic/review/', RentalCarReview_data, format='json')
        self.assertEqual(response.status_code, 201)
        # 비정상 처리 테스트 - 렌트카 리뷰 제목이 없을 경우
        RentalCarReview_data = {
            'title': '',
            'content': '렌트카 리뷰 내용',
            'star_score': '5',
            'rental_car': 1,
        }
        response = self.client.post('/traffic/review/', RentalCarReview_data, format='json')
        self.assertEqual(response.status_code, 400)
        # 비정상 처리 테스트 - 렌트카 리뷰 내용이 없을 경우
        RentalCarReview_data = {
            'title': '렌트카 리뷰 제목',
            'content': '',
            'star_score': '5',
            'rental_car': 1,
        }
        response = self.client.post('/traffic/review/', RentalCarReview_data, format='json')
        self.assertEqual(response.status_code, 400)
        # 비정상 처리 테스트 - 렌트카 리뷰 점수가 없을 경우
        RentalCarReview_data = {
            'title': '렌트카 리뷰 제목',
            'content': '렌트카 리뷰 내용',
            'star_score': '',
            'rental_car': 1,
        }
        response = self.client.post('/traffic/review/', RentalCarReview_data, format='json')
        self.assertEqual(response.status_code, 400)
        # 비정상 처리 테스트 - 렌트카 리뷰 점수가 0점일 경우
        RentalCarReview_data = {
            'title': '렌트카 리뷰 제목',
            'content': '렌트카 리뷰 내용',
            'star_score': '0',
            'rental_car': 1,
        }
        response = self.client.post('/traffic/review/', RentalCarReview_data, format='json')
        self.assertEqual(response.status_code, 400)
        print('-- 렌트카 리뷰 생성 테스트(일반 사용자) END --')

    def test_RentalCarReview_create(self):
        '''
        렌트카 리뷰 생성 테스트(로그인을 하지 않은 사용자)
        '''
        print('-- 렌트카 리뷰 생성 테스트(로그인을 하지 않은 사용자) BEGIN --')
        # 정상 처리 테스트
        RentalCarReview_data = {
            'title': '렌트카 리뷰 제목',
            'content': '렌트카 리뷰 내용',
            'star_score': '5',
            'rental_car': 1,
        }
        self.client.credentials()
        response = self.client.post('/traffic/review/', RentalCarReview_data, format='json')
        self.assertEqual(response.status_code, 401)
        print('-- 렌트카 리뷰 생성 테스트(로그인을 하지 않은 사용자) END --')

    def test_RentalCarReview_list(self):
        '''
        렌트카 리뷰 리스트 테스트
        '''
        print('-- 렌트카 리뷰 리스트 테스트 BEGIN --')
        self.client.credentials()
        response = self.client.get('/traffic/review/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)
        print('-- 렌트카 리뷰 리스트 테스트 END --')

    def test_RentalCarReview_update_user(self):
        '''
        렌트카 리뷰 수정 테스트(일반 사용자)
        '''
        print('-- 렌트카 리뷰 수정 테스트(일반 사용자) BEGIN --')
        # 정상 처리 테스트
        RentalCarReview_data = {
            'title': '렌트카 리뷰 제목123',
            'content': '렌트카 리뷰 내용1234567',
            'star_score': '5',
            'rental_car': 1,
            'user': 1,
        }
        response = self.client.put('/traffic/review/1/', RentalCarReview_data, format='json')
        self.assertEqual(response.status_code, 200)
        # 비정상 처리 테스트 - 존재하지 않는 렌트카 리뷰 수정 시도
        RentalCarReview_data = {
            'title': '렌트카 리뷰 제목123',
            'content': '렌트카 리뷰 내용1234567',
            'star_score': '5',
            'rental_car': 1,
            'user': 1,
        }
        response = self.client.put('/traffic/review/100/', RentalCarReview_data, format='json')
        self.assertEqual(response.status_code, 404)
        # 비정상 처리 테스트 - 렌트카 리뷰 제목이 없을 경우
        RentalCarReview_data = {
            'title': '',
            'content': '렌트카 리뷰 내용1234567',
            'star_score': '5',
            'rental_car': 1,
            'user': 1,
        }
        response = self.client.put('/traffic/review/1/', RentalCarReview_data, format='json')
        self.assertEqual(response.status_code, 400)
        # 비정상 처리 테스트 - 렌트카 리뷰 내용이 없을 경우
        RentalCarReview_data = {
            'title': '렌트카 리뷰 제목123',
            'content': '',
            'star_score': '5',
            'rental_car': 1,
            'user': 1,
        }
        response = self.client.put('/traffic/review/1/', RentalCarReview_data, format='json')
        self.assertEqual(response.status_code, 400)
        # 비정상 처리 테스트 - 렌트카 리뷰 점수가 없을 경우
        RentalCarReview_data = {
            'title': '렌트카 리뷰 제목123',
            'content': '렌트카 리뷰 내용1234567',
            'star_score': '',
            'rental_car': 1,
            'user': 1,
        }
        response = self.client.put('/traffic/review/1/', RentalCarReview_data, format='json')
        self.assertEqual(response.status_code, 400)
        # 비정상 처리 테스트 - 렌트카 리뷰 점수가 0점일 경우
        RentalCarReview_data = {
            'title': '렌트카 리뷰 제목123',
            'content': '렌트카 리뷰 내용1234567',
            'star_score': '0',
            'rental_car': 1,
            'user': 1,
        }
        response = self.client.put('/traffic/review/1/', RentalCarReview_data, format='json')
        self.assertEqual(response.status_code, 400)
        print('-- 렌트카 리뷰 수정 테스트(일반 사용자) END --')

    def test_RentalCarReview_update(self):
        '''
        렌트카 리뷰 수정 테스트(로그인을 하지 않은 사용자)
        '''
        print('-- 렌트카 리뷰 수정 테스트(로그인을 하지 않은 사용자) BEGIN --')
        # 비정상 처리 테스트 - 로그인을 하지 않은 사용자가 렌트카 리뷰 수정 시도
        RentalCarReview_data = {
            'title': '렌트카 리뷰 제목123',
            'content': '렌트카 리뷰 내용1234567',
            'star_score': '5',
            'rental_car': 1,
        }
        self.client.credentials()
        response = self.client.put('/traffic/review/1/')
        self.assertEqual(response.status_code, 401)
        print('-- 렌트카 리뷰 수정 테스트(로그인을 하지 않은 사용자) END --')

    def test_RentalCarReview_destroy_user(self):
        '''
        렌트카 리뷰 삭제 테스트(일반 사용자)
        '''
        print('-- 렌트카 리뷰 삭제 테스트(일반 사용자) BEGIN --')
        # 정상 처리 테스트
        response = self.client.delete('/traffic/review/1/')
        self.assertEqual(response.status_code, 204)
        print('-- 렌트카 리뷰 삭제 테스트(일반 사용자) END --')

    def test_RentalCarReview_destroy(self):
        '''
        렌트카 리뷰 삭제 테스트(로그인을 하지 않은 사용자)
        '''
        print('-- 렌트카 리뷰 삭제 테스트(로그인을 하지 않은 사용자) BEGIN --')
        # 비정상 처리 테스트 - 로그인을 하지 않은 사용자가 렌트카 리뷰 삭제 시도
        self.client.credentials()
        response = self.client.delete('/traffic/review/1/')
        self.assertEqual(response.status_code, 401)
        print('-- 렌트카 리뷰 삭제 테스트(로그인을 하지 않은 사용자) END --')

    def test_RentalCarReviewComment_create_user(self):
        '''
        렌트카 리뷰 댓글 생성 테스트(일반 사용자)
        '''
        print('-- 렌트카 리뷰 댓글 생성 테스트(일반 사용자) BEGIN --')
        # 정상 처리 테스트
        RentalCarReviewComment_data = {
            'content': '렌트카 리뷰 댓글 내용',
            'rental_car_review': 1,
            'user': 1,
        }
        response = self.client.post('/traffic/review/1/reply/', RentalCarReviewComment_data, format='json')
        self.assertEqual(response.status_code, 201)
        # 비정상 처리 테스트 - 렌트카 리뷰 댓글 내용이 없을 경우
        RentalCarReviewComment_data = {
            'content': '',
            'rental_car_review': 1,
            'user': 1,
        }
        response = self.client.post('/traffic/review/1/reply/', RentalCarReviewComment_data, format='json')
        self.assertEqual(response.status_code, 400)
        # 비정상 처리 테스트 - 존재하지 않는 렌트카 리뷰에 댓글 생성 시도
        RentalCarReviewComment_data = {
            'content': '렌트카 리뷰 댓글 내용',
            'rental_car_review': 100,
            'user': 1,
        }
        response = self.client.post('/traffic/review/100/reply/', RentalCarReviewComment_data, format='json')
        self.assertEqual(response.status_code, 400)
        print('-- 렌트카 리뷰 댓글 생성 테스트(일반 사용자) END --')

    def test_RentalCarReviewComment_create(self):
        '''
        렌트카 리뷰 댓글 생성 테스트(로그인을 하지 않은 사용자)
        '''
        print('-- 렌트카 리뷰 댓글 생성 테스트(로그인을 하지 않은 사용자) BEGIN --')
        # 정상 처리 테스트
        RentalCarReviewComment_data = {
            'content': '렌트카 리뷰 댓글 내용',
            'rental_car_review': 1,
        }
        self.client.credentials()
        response = self.client.post('/traffic/review/1/reply/', RentalCarReviewComment_data, format='json')
        self.assertEqual(response.status_code, 401)
        print('-- 렌트카 리뷰 댓글 생성 테스트(로그인을 하지 않은 사용자) END --')

    def test_RentalCarReviewComment_list(self):
        '''
        렌트카 리뷰 댓글 리스트 테스트
        '''
        print('-- 렌트카 리뷰 댓글 리스트 테스트 BEGIN --')
        self.client.credentials()
        response = self.client.get('/traffic/review/1/reply/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)
        print('-- 렌트카 리뷰 댓글 리스트 테스트 END --')

    def test_RentalCarReviewComment_update_user(self):
        '''
        렌트카 리뷰 댓글 수정 테스트(일반 사용자)
        '''
        print('-- 렌트카 리뷰 댓글 수정 테스트(일반 사용자) BEGIN --')
        # 정상 처리 테스트
        RentalCarReviewComment_data = {
            'content': '렌트카 리뷰 댓글 내용1234567',
            'rental_car_review': 1,
            'user': 1,
        }
        response = self.client.put('/traffic/review/1/reply/1/', RentalCarReviewComment_data, format='json')
        self.assertEqual(response.status_code, 200)
        # 비정상 처리 테스트 - 존재하지 않는 렌트카 리뷰 댓글 수정 시도
        RentalCarReviewComment_data = {
            'content': '렌트카 리뷰 댓글 내용1234567',
            'rental_car_review': 1,
            'user': 1,
        }
        response = self.client.put('/traffic/review/1/reply/100/', RentalCarReviewComment_data, format='json')
        self.assertEqual(response.status_code, 404)
        # 비정상 처리 테스트 - 렌트카 리뷰 댓글 내용이 없을 경우
        RentalCarReviewComment_data = {
            'content': '',
            'rental_car_review': 1,
            'user': 1,
        }
        response = self.client.put('/traffic/review/1/reply/1/', RentalCarReviewComment_data, format='json')
        self.assertEqual(response.status_code, 400)
        print('-- 렌트카 리뷰 댓글 수정 테스트(일반 사용자) END --')

    def test_RentalCarReviewComment_update(self):
        '''
        렌트카 리뷰 댓글 수정 테스트(로그인을 하지 않은 사용자)
        '''
        print('-- 렌트카 리뷰 댓글 수정 테스트(로그인을 하지 않은 사용자) BEGIN --')
        # 비정상 처리 테스트 - 로그인을 하지 않은 사용자가 렌트카 리뷰 댓글 수정 시도
        RentalCarReviewComment_data = {
            'content': '렌트카 리뷰 댓글 내용1234567',
            'rental_car_review': 1,
        }
        self.client.credentials()
        response = self.client.put('/traffic/review/1/reply/1/', RentalCarReviewComment_data, format='json')
        self.assertEqual(response.status_code, 401)
        print('-- 렌트카 리뷰 댓글 수정 테스트(로그인을 하지 않은 사용자) END --')

    def test_RentalCarReviewComment_destroy_user(self):
        '''
        렌트카 리뷰 댓글 삭제 테스트(일반 사용자)
        '''
        print('-- 렌트카 리뷰 댓글 삭제 테스트(일반 사용자) BEGIN --')
        # 정상 처리 테스트
        response = self.client.delete('/traffic/review/1/reply/1/')
        self.assertEqual(response.status_code, 204)
        # 비정상 처리 테스트 - 존재하지 않는 렌트카 리뷰 댓글 삭제 시도
        response = self.client.delete('/traffic/review/1/reply/100/')
        self.assertEqual(response.status_code, 404)
        print('-- 렌트카 리뷰 댓글 삭제 테스트(일반 사용자) END --')

    def test_RentalCarReviewComment_destroy(self):
        '''
        렌트카 리뷰 댓글 삭제 테스트(로그인을 하지 않은 사용자)
        '''
        print('-- 렌트카 리뷰 댓글 삭제 테스트(로그인을 하지 않은 사용자) BEGIN --')
        # 비정상 처리 테스트 - 로그인을 하지 않은 사용자가 렌트카 리뷰 댓글 삭제 시도
        self.client.credentials()
        response = self.client.delete('/traffic/review/1/reply/1/')
        self.assertEqual(response.status_code, 401)
        print('-- 렌트카 리뷰 댓글 삭제 테스트(로그인을 하지 않은 사용자) END --')

    def test_RentalCarReviewImage_create_user(self):
        '''
        렌트카 리뷰 이미지 생성 테스트(일반 사용자)
        '''
        print('-- 렌트카 리뷰 이미지 생성 테스트(일반 사용자) BEGIN --')
        # 정상 처리 테스트
        images = []
        for i in range(3):
            images.append(SimpleUploadedFile(name=f'test_image{i}.jpg', 
            content=open('static/assets/images/test_image/ormi.jpg', 'rb').read(), 
            content_type='image/jpeg'))
        RentalCarReview_data = {
            'title': '렌트카 리뷰 제목',
            'content': '렌트카 리뷰 내용',
            'star_score': '5',
            'rental_car': 1,
            'user': 1,
            'image': images,
        }
        response = self.client.post('/traffic/review/', RentalCarReview_data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(RentalCarReviewImage.objects.all().count(), 3)
        self.assertEqual(RentalCarReviewImage.objects.all()[0].rental_car_review.pk,11)
        self.assertEqual(RentalCarReview.objects.all()[10].rental_car_review_images.count(), 3)
        remove_media_folder()
        print('-- 렌트카 리뷰 이미지 생성 테스트(일반 사용자) END --')

    def test_RentalCarReviewImage_create(self):
        '''
        렌트카 리뷰 이미지 생성 테스트(로그인을 하지 않은 사용자)
        '''
        print('-- 렌트카 리뷰 이미지 생성 테스트(로그인을 하지 않은 사용자) BEGIN --')
        # 비정상 처리 테스트 - 로그인을 하지 않은 사용자가 렌트카 리뷰 이미지 생성 시도
        images = []
        for i in range(3):
            images.append(SimpleUploadedFile(name=f'test_image{i}.jpg', 
            content=open('static/assets/images/test_image/ormi.jpg', 'rb').read(), 
            content_type='image/jpeg'))
        RentalCarReview_data = {
            'title': '렌트카 리뷰 제목',
            'content': '렌트카 리뷰 내용',
            'star_score': '5',
            'rental_car': 1,
            'image': images,
        }
        self.client.credentials()
        response = self.client.post('/traffic/review/', RentalCarReview_data, format='multipart')
        self.assertEqual(response.status_code, 401)
        print('-- 렌트카 리뷰 이미지 생성 테스트(로그인을 하지 않은 사용자) END --')

    def test_RentalCarReviewImage_destroy_user(self):
        '''
        렌트카 리뷰 이미지 삭제 테스트(일반 사용자)
        '''
        print('-- 렌트카 리뷰 이미지 삭제 테스트(일반 사용자) BEGIN --')
        # 정상 처리 테스트
        images = []
        for i in range(3):
            images.append(SimpleUploadedFile(name=f'test_image{i}.jpg', 
            content=open('static/assets/images/test_image/ormi.jpg', 'rb').read(), 
            content_type='image/jpeg'))
        RentalCarReview_data = {
            'title': '렌트카 리뷰 제목',
            'content': '렌트카 리뷰 내용',
            'star_score': '5',
            'rental_car': 1,
            'user': 1,
            'image': images,
        }
        response = self.client.post('/traffic/review/', RentalCarReview_data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(RentalCarReviewImage.objects.all().count(), 3)
        self.assertEqual(RentalCarReviewImage.objects.all()[0].rental_car_review.pk,11)
        self.assertEqual(RentalCarReview.objects.all()[10].rental_car_review_images.count(), 3)
        response = self.client.delete('/traffic/review/image/1/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(RentalCarReviewImage.objects.all().count(), 2)
        response = self.client.delete('/traffic/review/image/2/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(RentalCarReview.objects.all()[10].rental_car_review_images.count(), 1)
        # 비정상 처리 테스트 - 존재하지 않는 렌트카 리뷰 이미지 삭제 시도
        response = self.client.delete('/traffic/review/image/100/')
        self.assertEqual(response.status_code, 404)
        remove_media_folder()
        print('-- 렌트카 리뷰 이미지 삭제 테스트(일반 사용자) END --')

    def test_RentalCarReviewImage_destroy(self):
        '''
        렌트카 리뷰 이미지 삭제 테스트(로그인을 하지 않은 사용자)
        '''
        print('-- 렌트카 리뷰 이미지 삭제 테스트(로그인을 하지 않은 사용자) BEGIN --')
        # 비정상 처리 테스트 - 로그인을 하지 않은 사용자가 렌트카 리뷰 이미지 삭제 시도
        self.client.credentials()
        response = self.client.delete('/traffic/review/image/1/')
        self.assertEqual(response.status_code, 401)
        print('-- 렌트카 리뷰 이미지 삭제 테스트(로그인을 하지 않은 사용자) END --')