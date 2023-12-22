from .test_setup import LogingTestCase

class LocationTestCase(LogingTestCase):
    def setUp(self):
        super().setUp()

    def test_create_main_location(self):
        '''
        메인 지역 CRUD 테스트
        '''
        print('-- 메인 지역 생성 테스트 BEGIN --')
        # 메인 지역 생성 테스트
        data = {
            'address': '테스트 메인 지역',
        }
        response = self.client.post(
            '/lodging/mainlocation/', 
            data, 
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}', 
            format='json')
        self.assertEqual(response.status_code, 201)

        # 메인 지역 생성 테스트 - 주소 없음
        data = {
            'address': '',
        }
        response = self.client.post(
            '/lodging/mainlocation/', 
            data, 
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}', 
            format='json')
        self.assertEqual(response.status_code, 400)
        print('-- 메인 지역 생성 테스트 END --')

        print('-- 메인 지역 조회 테스트 BEGIN --')
        # 메인 지역 조회 테스트
        response = self.client.get('/lodging/mainlocation/')
        self.assertEqual(response.status_code, 200)
        print('-- 메인 지역 조회 테스트 END --')

        print('-- 메인 지역 수정 테스트 BEGIN --')
        # 메인 지역 수정 테스트
        data = {
            'address': '서울시 강동구 천호동',
        }
        response = self.client.patch(
            '/lodging/mainlocation/1/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json',)
        self.assertEqual(response.status_code, 200)

        # 메인 지역 수정 테스트 - 주소 없음
        data = {
            'address': '',
        }
        response = self.client.patch(
            '/lodging/mainlocation/1/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json',)
        self.assertEqual(response.status_code, 400)
        print('-- 메인 지역 수정 테스트 END --')

        print('-- 메인 지역 삭제 테스트 BEGIN --')
        # 메인 지역 삭제 테스트
        response = self.client.delete(
            '/lodging/mainlocation/2/',
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json',)
        self.assertEqual(response.status_code, 204)


    def test_sub_location(self):
        '''
        서브 지역 CRUD 테스트
        '''
        print('-- 서브 지역 생성 테스트 BEGIN --')
        # 서브 지역 생성 테스트
        data = {
            'address': '테스트 서브 지역',
            'main_location': 1,
        }
        response = self.client.post(
            '/lodging/sublocation/', 
            data, 
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}', 
            format='json')
        self.assertEqual(response.status_code, 201)

        # 서브 지역 생성 테스트 - 주소 없음
        data = {
            'address': '',
            'main_location': 1,
        }
        response = self.client.post(
            '/lodging/sublocation/', 
            data, 
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}', 
            format='json')
        self.assertEqual(response.status_code, 400)

        # 서브 지역 생성 테스트 - 메인 지역 없음
        data = {
            'address': '테스트 서브 지역',
            'main_location': 100,
        }
        response = self.client.post(
            '/lodging/sublocation/', 
            data, 
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}', 
            format='json')
        self.assertEqual(response.status_code, 400)
        print('-- 서브 지역 생성 테스트 END --')

        print('-- 서브 지역 조회 테스트 BEGIN --')
        # 서브 지역 조회 테스트
        response = self.client.get('/lodging/sublocation/')
        self.assertEqual(response.status_code, 200)
        print('-- 서브 지역 조회 테스트 END --')
        
        print('-- 서브 지역 수정 테스트 BEGIN --')
        # 서브 지역 수정 테스트
        data = {
            'address': '테스트 서브 지역 수정',
            'main_location': 1,
        }
        response = self.client.patch(
            '/lodging/sublocation/1/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json',)
        self.assertEqual(response.status_code, 200)

        # 서브 지역 수정 테스트 - 주소 없음
        data = {
            'address': '',
            'main_location': 1,
        }
        response = self.client.patch(
            '/lodging/sublocation/1/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json',)
        self.assertEqual(response.status_code, 400)

        # 서브 지역 수정 테스트 - 메인 지역 없음
        data = {
            'address': '테스트 서브 지역 수정',
            'main_location': 100,
        }
        response = self.client.patch(
            '/lodging/sublocation/1/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json',)
        self.assertEqual(response.status_code, 400)
        print('-- 서브 지역 수정 테스트 END --')

        print('-- 서브 지역 삭제 테스트 BEGIN --')
        # 서브 지역 삭제 테스트
        response = self.client.delete(
            '/lodging/sublocation/2/',
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json',)
        self.assertEqual(response.status_code, 204)
        print('-- 서브 지역 삭제 테스트 END --')
        