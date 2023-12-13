import base64
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from .models import CustomUser as User

class TestAccount(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_account_signup(self):
        '''
        회원가입 테스트
        1. 이메일 유효성 테스트
        2. 비밀번호 유효성 테스트
            - 8글자 이상
            - 15글자 이하
            - 숫자 포함
            - 특수문자 포함
            - 확인 비밀번호와 일치
        3. 중복 이메일 테스트
        4. 별명 중복 테스트
        '''
        print('-- 회원가입 테스트 BEGIN --')
        # 이메일 유효성 테스트 - 이메일 형식
        data = {
            'email': 'test',
            'username': 'test',
            'nickname': 'test',
            'password': 'testtest1@',
            'password2': 'testtest1@',
        }
        response = self.client.post(
            '/account/signup/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['email'][0], '유효한 이메일 주소를 입력하십시오.')

        # 비밀번호 유효성 테스트 - 8글자 이상
        data = {
            'email': 'test@gmail.com',
            'username': 'test',
            'nickname': 'test',
            'password': 'test1@',
            'password2': 'test1@',
        }
        response = self.client.post(
            '/account/signup/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'][0], '비밀번호는 8글자 이상 15글자 이하로 입력해주세요.')

        # 비밀번호 유효성 테스트 - 15글자 이하
        data = {
            'email': 'test@gmail.com',
            'username': 'test',
            'nickname': 'test',
            'password': 'testtesttesttest1@',
            'password2': 'testtesttesttest1@',
        }
        response = self.client.post(
            '/account/signup/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'][0], '비밀번호는 8글자 이상 15글자 이하로 입력해주세요.')

        # 비밀번호 유효성 테스트 - 숫자 포함
        data = {
            'email': 'test@gmail.com',
            'username': 'test',
            'nickname': 'test',
            'password': 'testtesttest!',
            'password2': 'testtesttest!',
        }
        response = self.client.post(
            '/account/signup/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'][0], '비밀번호는 숫자를 포함해야 합니다.')

        # 비밀번호 유효성 테스트 - 특수문자 포함
        data = {
            'email': 'test@gmail.com',
            'username': 'test',
            'nickname': 'test',
            'password': 'testtesttest1',
            'password2': 'testtesttest1',
        }
        response = self.client.post(
            '/account/signup/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'][0], '비밀번호는 특수문자를 포함해야 합니다.')

        # 비밀번호 유효성 테스트 - 확인 비밀번호와 일치
        data = {
            'email': 'test@gmail.com',
            'username': 'test',
            'nickname': 'test',
            'password': 'testtesttest1!',
            'password2': 'testtesttest2@',
        }
        response = self.client.post(
            '/account/signup/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'][0], '비밀번호가 일치하지 않습니다.')

        # 회원가입 정상 처리 테스트
        image = SimpleUploadedFile(name='test_image.jpg', 
                                content=open('static/assets/images/test_image/ormi.jpg', 'rb').read(), 
                                content_type='image/jpeg')
        data = {
            'email': 'test@gmail.com',
            'username': 'test',
            'nickname': 'test',
            'password': 'testtest1@',
            'password2': 'testtest1@',
            'image': image,
        }
        response = self.client.post(
            '/account/signup/', 
            data,
            format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(id=1).email, 'test@gmail.com')
        self.assertEqual(User.objects.get(id=1).username, 'test')

        # 중복 이메일 테스트
        data = {
            'email': 'test@gmail.com',
            'username': 'test',
            'nickname': 'test2',
            'password': 'testtest1@',
            'password2': 'testtest1@',
        }
        response = self.client.post(
            '/account/signup/', 
            data,
            format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['email'][0], '이미 사용중인 이메일입니다.')

        # 중복 별명 테스트
        data = {
            'email': 'test2@gmail.com',
            'username': 'test',
            'nickname': 'test',
            'password': 'testtest1@',
            'password2': 'testtest1@',
        }
        response = self.client.post(
            '/account/signup/', 
            data,
            format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['nickname'][0], '이미 사용중인 별명입니다.')
        print('-- 회원가입 테스트 END --')