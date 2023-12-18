from .test_setup import LogingTestCase

class AmenityTestCase(LogingTestCase):
    def setUp(self):
        super().setUp()

    def test_create_amenity(self):
        '''
        편의시설 CRUD 테스트
        '''
        print('-- 편의시설 생성 테스트 BEGIN --')
        # 편의시설 생성 테스트
        data = {
            'name': '테스트 편의시설',
            'lodging': 1,
        }
        response = self.client.post(
            '/lodging/amenity/', 
            data, 
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}', 
            format='json')
        self.assertEqual(response.status_code, 201)

        # 편의시설 생성 테스트 - 숙소 없음
        data = {
            'name': '테스트 편의시설',
            'lodging': 100,
        }
        response = self.client.post(
            '/lodging/amenity/', 
            data, 
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}', 
            format='json')
        self.assertEqual(response.status_code, 400)

        # 편의시설 생성 테스트 - admin 권한 없는 사용자
        data = {
            'name': '테스트 편의시설',
            'lodging': 1,
        }
        response = self.client.post(
            '/lodging/amenity/', 
            data, 
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}', 
            format='json')
        self.assertEqual(response.status_code, 403)

        # 편의시설 생성 테스트 - 편의시설 이름 없음
        data = {
            'name': '',
            'lodging': 1,
        }
        response = self.client.post(
            '/lodging/amenity/', 
            data, 
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}', 
            format='json')
        self.assertEqual(response.status_code, 400)
        print('-- 편의시설 생성 테스트 END --')

        print('-- 편의시설 수정 테스트 BEGIN --')
        # 편의시설 수정 테스트
        data = {
            'name': '테스트 편의시설 수정',
            'lodging': 1,
        }
        response = self.client.patch(
            '/lodging/amenity/1/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json')
        self.assertEqual(response.status_code, 200)

        # 편의시설 수정 테스트 - 숙소 없음
        data = {
            'name': '테스트 편의시설 수정',
            'lodging': 100,
        }
        response = self.client.patch(
            '/lodging/amenity/1/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json')
        self.assertEqual(response.status_code, 400)

        # 편의시설 수정 테스트 - admin 권한 없는 사용자
        data = {
            'name': '테스트 편의시설 수정',
            'lodging': 1,
        }
        response = self.client.patch(
            '/lodging/amenity/1/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json')
        self.assertEqual(response.status_code, 403)
        print('-- 편의시설 수정 테스트 END --')

        print('-- 편의시설 리스트 테스트 BEGIN --')
        # 편의시설 리스트 테스트
        response = self.client.get('/lodging/amenity/')
        self.assertEqual(response.status_code, 200)
        print('-- 편의시설 리스트 테스트 END --')

        print('-- 편의시설 삭제 테스트 BEGIN --')
        # 편의시설 삭제 테스트 - 편의시설 없음
        response = self.client.delete(
            '/lodging/amenity/100/',
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json')
        self.assertEqual(response.status_code, 404)

        # 편의시설 삭제 테스트 - admin 권한 없는 사용자
        response = self.client.delete(
            '/lodging/amenity/1/',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            format='json')
        self.assertEqual(response.status_code, 403)

        # 편의시설 삭제 테스트
        response = self.client.delete(
            '/lodging/amenity/1/',
            HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}',
            format='json')
        self.assertEqual(response.status_code, 204)
        print('-- 편의시설 삭제 테스트 END --')