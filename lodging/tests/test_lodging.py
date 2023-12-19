from .test_setup import LogingTestCase

class LodgingTestCase(LogingTestCase):
    def setUp(self):
        super().setUp_lodging()

    def test_lodging_create_admin(self):
        '''
        숙소 생성 테스트 - admin 권한 사용자
        
        '''
        print('-- 숙소 생성 테스트 - admin 권한 사용자 BEGIN --')
        self.client.force_authenticate(user=self.admin)

        response = self.client.post('/lodging/', self.lodging_data, format='json')
        self.assertEqual(response.status_code, 201)
        print('-- 숙소 생성 테스트 - admin 권한 사용자 END --')

    def test_lodging_create_user(self):
        '''
        숙소 생성 테스트 - user 권한 사용자
        '''
        print('-- 숙소 생성 테스트 - user 권한 사용자 BEGIN --')
        self.client.force_login(user=self.user)
        response = self.client.post('/lodging/', self.lodging_data, format='json')
        self.assertEqual(response.status_code, 401)
        print('-- 숙소 생성 테스트 - user 권한 사용자 END --')

    def test_lodging_create_no_auth(self):
        '''
        숙소 생성 테스트 - 권한 없는 사용자
        '''
        print('-- 숙소 생성 테스트 - 권한 없는 사용자 BEGIN --')
        response = self.client.post('/lodging/', self.lodging_data, format='json')
        self.assertEqual(response.status_code, 401)
        print('-- 숙소 생성 테스트 - 권한 없는 사용자 END --')
    
    def test_lodging_no_data_create(self):
        '''
        숙소 생성 에러 테스트 - name 필드 누락
        '''
        print('-- 숙소 생성 에러 테스트 BEGIN --')
        self.client.force_authenticate(user=self.admin)

        lodging_no_data = {
            'name': '',
            'intro': '테스트 숙소 소개',
            'notice': '테스트 숙소 주의사항',
            'info': '테스트 숙소 정보',
            'sub_location': 1,
        }

        response = self.client.post('/lodging/', lodging_no_data, format='json')
        self.assertEqual(response.status_code, 400)
        print('-- 숙소 생성 에러 테스트 END --')

    def test_lodging_update_admin(self):
        '''
        숙소 수정 테스트 - admin 권한 사용자
        '''
        print('-- admin 권한 사용자 숙소 수정 테스트 BEGIN --')
        self.client.force_authenticate(user=self.admin)

        response = self.client.patch('/lodging/1/', self.updated_data, format='json')
        self.assertEqual(response.status_code, 200)

        '''
        존재하지 않는 숙소 수정 테스트 - admin 권한 사용자
        '''
        response = self.client.patch('/lodging/2/', self.updated_data, format='json')
        self.assertEqual(response.status_code, 404)
        print('-- admin 권한 사용자 숙소 수정 테스트 END --')

    def test_lodging_update_user(self): 
        '''
        숙소 수정 테스트 - user 권한 사용자
        '''
        print('-- user 권한 사용자 숙소 수정 테스트 BEGIN --')
        self.client.force_login(user=self.user)

        response = self.client.patch('/lodging/1/', self.updated_data, format='json')
        self.assertEqual(response.status_code, 401)
        print('-- user 권한 사용자 숙소 수정 테스트 END --')

    def test_lodging_update_no_auth(self):
        '''
        숙소 수정 테스트 - 권한 없는 사용자
        '''
        print('-- 권한 없는 사용자 숙소 수정 테스트 BEGIN --')
        response = self.client.put('/lodging/1/', self.updated_data, format='json')
        self.assertEqual(response.status_code, 401)
        print('-- 권한 없는 사용자 숙소 수정 테스트 END --')

    def test_lodging_list(self):
        '''
        숙소 리스트 테스트
        '''
        print('-- 숙소 리스트 테스트 BEGIN --')
        response = self.client.get('/lodging/', format='json')
        self.assertEqual(response.status_code, 200)
        print('-- 숙소 리스트 테스트 END --')

    def test_lodging_retrieve(self):
        '''
        숙소 조회 테스트
        '''
        print('-- 숙소 조회 테스트 BEGIN --')
        response = self.client.get('/lodging/1/', format='json')
        self.assertEqual(response.status_code, 200)

        '''
        존재하지 않는 숙소 조회 테스트
        '''
        response = self.client.get('/lodging/2/', format='json')
        self.assertEqual(response.status_code, 404)
        print('-- 숙소 조회 테스트 END --')
    
    def test_lodging_delete_admin(self):
        '''
        숙소 삭제 테스트 - admin 권한 사용자
        '''
        print('-- 숙소 삭제 테스트 BEGIN --')
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete('/lodging/1/', format='json')
        self.assertEqual(response.status_code, 204)

        '''
        존재하지 않는 숙소 삭제 테스트
        '''
        response = self.client.delete('/lodging/2/', format='json')
        self.assertEqual(response.status_code, 404)
        print('-- 숙소 삭제 테스트 END --')
        