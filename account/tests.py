from datetime import datetime, timedelta
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

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
        # image = SimpleUploadedFile(name='test_image.jpg', 
        #                         content=open('static/assets/images/test_image/ormi.jpg', 'rb').read(), 
        #                         content_type='image/jpeg')
        data = {
            'email': 'test@gmail.com',
            'username': 'test',
            'nickname': 'test',
            'password': 'testtest1@',
            'password2': 'testtest1@',
            # 'image': image,
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

    def test_account_login(self): 
        '''
        로그인 테스트
        1. 정상 로그인 테스트
        2. 없는 사용자 테스트
        3. 비밀번호 불일치 테스트
        4. 이메일을 입력하지 않은 경우 테스트
        5. 비밀번호를 입력하지 않은 경우 테스트
        '''
        print('-- 로그인 테스트 BEGIN --')
        data = {
            'email': 'test@gmail.com',
            'username': 'test',
            'nickname': 'test',
            'password': 'testtest1@',
            'password2': 'testtest1@',
        }
        self.client.post(
            '/account/signup/', 
            data,
            format='multipart')
        # 정상 로그인 테스트
        data = {
            'email': 'test@gmail.com',
            'password': 'testtest1@',
        }
        response = self.client.post(
            '/account/login/',
            data,
            format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['refresh'])
        self.assertTrue(response.data['access'])

        # 없는 사용자 테스트
        data = {
            'email': 'test1@gmail.com',
            'password': 'testtest1@',
        }
        response = self.client.post(
            '/account/login/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '이메일 또는 비밀번호가 일치하지 않습니다.')

        # 비밀번호 불일치 테스트
        data = {
            'email': 'test@gmail.com',
            'password': 'testtest1!',
        }
        response = self.client.post(
            '/account/login/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '이메일 또는 비밀번호가 일치하지 않습니다.')

        # 이메일을 입력하지 않은 경우 테스트
        data = {
            'password': 'testtest1@',
        }
        response = self.client.post(
            '/account/login/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['email'][0], '이메일을 입력해주세요.')

        # 비밀번호를 입력하지 않은 경우 테스트
        data = {
            'email': 'test@gmail.com',
        }
        response = self.client.post(
            '/account/login/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'][0], '비밀번호를 입력해주세요.')
        print('-- 로그인 테스트 END --')

    def test_token_expiration(self):
        '''
        토큰 만료 테스트
        '''
        print('-- 토큰 만료 테스트 BEGIN --')
        user = User.objects.create_user(email='test@test.com', password='testtest1@')
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        refresh_exp = datetime.now() + timedelta(weeks=1)
        access_exp = datetime.now() + timedelta(days=1)

        refresh_token = refresh_token.set_exp(refresh_exp)
        access_token = access_token.set_exp(access_exp)

        refresh_token = str(refresh_token)
        access_token = str(access_token)

        try:
            RefreshToken(refresh_token)
            is_valid = True
        except:
            is_valid = False
        self.assertFalse(is_valid)
    
        try:
            RefreshToken(access_token)
            is_valid = True
        except:
            is_valid = False
        self.assertFalse(is_valid)
        print('-- 토큰 만료 테스트 END --')

    def test_token_refresh(self):
        '''
        토큰 재발급 테스트
        1. 정상 토큰 재발급 테스트
        2. 만료된 토큰 재발급 테스트
        '''
        print('-- 토큰 재발급 테스트 BEGIN --')
        user = User.objects.create_user(email='test@test.com', password='testtest1@')
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        access_exp = datetime.now() + timedelta(days=1)

        access_token = access_token.set_exp(access_exp)

        # 정상 토큰 재발급 테스트
        response = self.client.post(
            '/account/refresh/',
            {'refresh': str(refresh_token)},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['access'])
        new_access_token = response.data['access']
        try:
            AccessToken(new_access_token)
            is_valid = True
        except:
            is_valid = False
        self.assertTrue(is_valid)

        # 만료된 토큰 재발급 테스트
        refresh_exp = datetime.now() + timedelta(weeks=1)
        refresh_token = refresh_token.set_exp(refresh_exp)
        response = self.client.post(
            '/account/refresh/',
            {'refresh': str(refresh_token)},
            format='json'
        )
        self.assertEqual(response.status_code, 401)
        print('-- 토큰 재발급 테스트 END --')

    def test_account_profile_get(self):
        '''
        프로필 조회 테스트
        1. 미로그인 사용자 프로필 조회 테스트
        2. 로그인 & 권한X 사용자 프로필 조회 테스트
        3. 로그인 & 권한O 사용자 프로필 조회 테스트
        '''
        print('-- 프로필 조회 테스트 BEGIN --')
        data = {
            'email': 'test@gmail.com',
            'username': 'test',
            'nickname': 'test',
            'password': 'testtest1@',
            'password2': 'testtest1@',
        }
        self.client.post(
            '/account/signup/', 
            data,
            format='multipart')
        data = {
            'email': 'test1@gmail.com',
            'username': 'test',
            'nickname': 'test1',
            'password': 'testtest1@',
            'password2': 'testtest1@',
        }
        self.client.post(
            '/account/signup/', 
            data,
            format='multipart')
        # 미로그인 사용자 프로필 조회 테스트
        response = self.client.get('/account/1/',
                        format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '로그인이 필요합니다.')

        # 로그인 & 권한X 사용자 프로필 조회 테스트
        data = {
            'email': 'test1@gmail.com',
            'password': 'testtest1@',
        }
        login_response = self.client.post(
            '/account/login/',
            data,
            format='json')
        access_token = login_response.data['access']
        response = self.client.get('/account/1/',
            HTTP_AUTHORIZATION=f'Bearer {access_token}',
            format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], '권한이 없습니다.')

        # 로그인 & 권한O 사용자 프로필 조회 테스트
        data = {
            'email': 'test@gmail.com',
            'password': 'testtest1@',
        }
        login_response = self.client.post(
            '/account/login/',
            data,
            format='json')
        access_token = login_response.data['access']
        response = self.client.get('/account/1/',
            HTTP_AUTHORIZATION=f'Bearer {access_token}',
            format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'test')
        print('-- 프로필 조회 테스트 END --')

    def test_account_profile_put(self):
        '''
        프로필 수정 테스트
        1. 미로그인 사용자 프로필 수정 테스트
        2. 로그인 & 권한X 사용자 프로필 수정 테스트
        3. 로그인 & 권한O 사용자 프로필 수정 테스트
        4. 닉네임 유효성 테스트
            - 이전 닉네임과 같은 경우
            - 이미 사용중인 닉네임인 경우
            - 입력하지 않은 경우
        '''
        print('-- 프로필 수정 테스트 BEGIN --')
        data = {
            'email': 'test@gmail.com',
            'username': 'test',
            'nickname': 'test',
            'password': 'testtest1@',
            'password2': 'testtest1@',
        }
        self.client.post(
            '/account/signup/', 
            data,
            format='multipart')
        data = {
            'email': 'test1@gmail.com',
            'username': 'test',
            'nickname': 'test1',
            'password': 'testtest1@',
            'password2': 'testtest1@',
        }
        self.client.post(
            '/account/signup/', 
            data,
            format='multipart')
        # 미로그인 사용자 프로필 수정 테스트
        data = {
            'nickname': 'test2',
        }
        response = self.client.patch('/account/1/',
                        data,
                        format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '로그인이 필요합니다.')

        # 로그인 & 권한X 사용자 프로필 수정 테스트
        data = {
            'email': 'test1@gmail.com',
            'password': 'testtest1@',
        }
        login_response = self.client.post(
            '/account/login/',
            data,
            format='json')
        access_token = login_response.data['access']
        data = {
            'nickname': 'test2',
        }
        response = self.client.patch('/account/1/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {access_token}',
            format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], '권한이 없습니다.')

        # 로그인 & 권한O 사용자 프로필 수정 테스트
        data = {
            'email': 'test@gmail.com',
            'password': 'testtest1@',
        }
        login_response = self.client.post(
            '/account/login/',
            data,
            format='json')
        access_token = login_response.data['access']
        # image = SimpleUploadedFile(name='test_image.jpg', 
        #                         content=open('static/assets/images/test_image/ormi.jpg', 'rb').read(), 
        #                         content_type='image/jpeg')
        data = {
            'nickname': 'test2',
            # 'image': image,
        }
        response = self.client.patch('/account/1/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {access_token}',
            format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(pk=1)[0].nickname, 'test2')
        # self.assertTrue(User.objects.filter(pk=1)[0].image.url)

        # 닉네임 유효성 테스트 - 이전 닉네임과 같은 경우
        data = {
            'email': 'test@gmail.com',
            'password': 'testtest1@',
        }
        login_response = self.client.post(
            '/account/login/',
            data,
            format='json')
        access_token = login_response.data['access']
        data = {
            'nickname': 'test2',
        }
        response = self.client.patch('/account/1/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {access_token}',
            format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['nickname'][0], '이전 별명과 같습니다.')

        # 닉네임 유효성 테스트 - 이미 사용중인 닉네임인 경우
        data = {
            'email': 'test@gmail.com',
            'password': 'testtest1@',
        }
        login_response = self.client.post(
            '/account/login/',
            data,
            format='json')
        access_token = login_response.data['access']
        data = {
            'nickname': 'test1',
        }
        response = self.client.patch('/account/1/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {access_token}',
            format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['nickname'][0], '이미 사용중인 별명입니다.')

        # 닉네임 유효성 테스트 - 입력하지 않은 경우
        data = {
            'email': 'test@gmail.com',
            'password': 'testtest1@',
        }
        login_response = self.client.post(
            '/account/login/',
            data,
            format='json')
        access_token = login_response.data['access']
        data = {
            'nickname': '',
        }
        response = self.client.patch('/account/1/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {access_token}',
            format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['nickname'][0], '별명을 입력해주세요.')

        print('-- 프로필 수정 테스트 END --')

    def test_account_secession(self):
        '''
        회원탈퇴 테스트
        1. 미로그인 사용자 회원탈퇴 테스트
        2. 로그인 & 권한X 사용자 회원탈퇴 테스트
        3. 로그인 & 권한O 사용자 회원탈퇴 테스트
        '''
        print('-- 회원탈퇴 테스트 BEGIN --')
        data = {
            'email': 'test@gmail.com',
            'username': 'test',
            'nickname': 'test',
            'password': 'testtest1@',
            'password2': 'testtest1@',
        }
        self.client.post(
            '/account/signup/', 
            data,
            format='json')
        data = {
            'email': 'test1@gmail.com',
            'username': 'test',
            'nickname': 'test1',
            'password': 'testtest1@',
            'password2': 'testtest1@',
        }
        self.client.post(
            '/account/signup/', 
            data,
            format='json')
        
        # 미로그인 사용자 회원탈퇴 테스트
        response = self.client.delete(
            '/account/1/',
            format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '로그인이 필요합니다.')

        # 로그인 & 권한X 사용자 회원탈퇴 테스트
        response = self.client.post(
            '/account/login/',
            {'email': 'test1@gmail.com', 'password': 'testtest1@'},
            format='json')
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.delete(
            '/account/1/',
            format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], '권한이 없습니다.')

        # 로그인 & 권한O 사용자 회원탈퇴 테스트
        response = self.client.post(
            '/account/login/',
            {'email': 'test@gmail.com', 'password': 'testtest1@'},
            format='json')
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.delete(
            '/account/1/',
            format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.count(), 1)

        print('-- 회원탈퇴 테스트 END --')

    def test_account_password_change(self):
        '''
        비밀번호 변경 테스트
        1. 미로그인 사용자 비밀번호 변경 테스트
        2. 로그인 & 권한X 사용자 비밀번호 변경 테스트
        3. 비밀번호 유효성 테스트
            - 8글자 이상
            - 15글자 이하
            - 숫자 포함
            - 특수문자 포함
            - 확인 비밀번호와 일치
        4. 로그인 & 권한O 사용자(기존 비밀번호 불일치) 비밀번호 변경 테스트
        5. 로그인 & 권한O 사용자(기존 비밀번호 일치) 비밀번호 변경 테스트
        '''
        print('-- 비밀번호 변경 테스트 BEGIN --')
        data = {
            'email': 'test@gmail.com',
            'username': 'test',
            'nickname': 'test',
            'password': 'testtest1@',
            'password2': 'testtest1@',
        }
        self.client.post(
            '/account/signup/', 
            data,
            format='json')
        data = {
            'email': 'test1@gmail.com',
            'username': 'test',
            'nickname': 'test1',
            'password': 'testtest1@',
            'password2': 'testtest1@',
        }
        self.client.post(
            '/account/signup/', 
            data,
            format='json')
        # 미로그인 사용자 비밀번호 변경 테스트
        response = self.client.patch(
            '/account/1/password/',
            {'old_password': 'testtest1@', 'password': 'testtest2@', 'password2': 'testtest2@'},
            format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], '로그인이 필요합니다.')

        # 로그인 & 권한X 사용자 비밀번호 변경 테스트
        response = self.client.post(
            '/account/login/',
            {'email': 'test1@gmail.com',
            'password': 'testtest1@'},
            format='json')
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.patch(
            '/account/1/password/',
            {'old_password': 'testtest1@', 'password': 'testtest2@', 'password2': 'testtest2@'},
            format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], '권한이 없습니다.')

        # 비밀번호 유효성 테스트 - 8글자 이상
        response = self.client.post(
            '/account/login/',
            {'email': 'test@gmail.com',
            'password': 'testtest1@'},
            format='json')
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        data = {
            'old_password': 'testtest1@',
            'password': 'test1@',
            'password2': 'test1@',
        }
        response = self.client.patch(
            '/account/1/password/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'][0], '비밀번호는 8글자 이상 15글자 이하로 입력해주세요.')

        # 비밀번호 유효성 테스트 - 15글자 이하
        data = {
            'old_password': 'testtest1@',
            'password': 'testtesttesttest1@',
            'password2': 'testtesttesttest1@',
        }
        response = self.client.patch(
            '/account/1/password/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'][0], '비밀번호는 8글자 이상 15글자 이하로 입력해주세요.')

        # 비밀번호 유효성 테스트 - 숫자 포함
        data = {
            'old_password': 'testtest1@',
            'password': 'testtesttest!',
            'password2': 'testtesttest!',
        }
        response = self.client.patch(
            '/account/1/password/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'][0], '비밀번호는 숫자를 포함해야 합니다.')

        # 비밀번호 유효성 테스트 - 특수문자 포함
        data = {
            'old_password': 'testtest1@',
            'password': 'testtesttest1',
            'password2': 'testtesttest1',
        }
        response = self.client.patch(
            '/account/1/password/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'][0], '비밀번호는 특수문자를 포함해야 합니다.')

        # 비밀번호 유효성 테스트 - 확인 비밀번호와 일치
        data = {
            'old_password': 'testtest1@',
            'password': 'testtesttest1!',
            'password2': 'testtesttest2@',
        }
        response = self.client.patch(
            '/account/1/password/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'][0], '비밀번호가 일치하지 않습니다.')

        # 로그인 & 권한O 사용자(기존 비밀번호 불일치) 비밀번호 변경 테스트
        response = self.client.patch(
            '/account/1/password/',
            {'old_password': 'testtest2@', 'password': 'testtest3@', 'password2': 'testtest3@'},
            format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['old_password'][0], '기존 비밀번호가 일치하지 않습니다.')
        
        # 로그인 & 권한O 사용자(기존 비밀번호 일치) 비밀번호 변경 테스트
        response = self.client.patch(
            '/account/1/password/',
            {'old_password': 'testtest1@', 'password': 'testtest3@', 'password2': 'testtest3@'},
            format='json')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            '/account/login/',
            {'email': 'test@gmail.com',
            'password': 'testtest3@'},
            format='json')
        self.assertEqual(response.status_code, 200)
        print('-- 비밀번호 변경 테스트 END --')