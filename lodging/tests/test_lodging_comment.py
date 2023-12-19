from .test_setup import LogingTestCase

class LodgingCommentTest(LogingTestCase):
    def setUp(self):
        super().setUp_lodging_comment()
    
    def test_create_lodging_review_comment(self):
        '''
        숙소 리뷰 댓글 CRUD 테스트
        '''
        print('숙소 리뷰 댓글 생성 테스트 - Begin')
        
        # 숙소 리뷰 댓글 생성 테스트 - 인증X
        data = {
            'content': 'test content',
            'lodging_review': 1,
            'user': 1,
        }

        response = self.client.post(
            '/lodging/review/1/comment/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 401)

        #숙소 리뷰 댓글 생성 테스트 - 인증O
        data = {
            'content': 'test content',
            'lodging_review': 1,
            'user': 1,
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(
            '/lodging/review/1/comment/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 201)

        #숙소 리뷰 댓글 생성 테스트 - 숙소 리뷰 없음
        data = {
            'content': 'test content',
            'lodging_review': 100,
            'user': 1,
        }
        response = self.client.post(
            '/lodging/review/100/comment/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 400)

        #숙소 리뷰 댓글 생성 테스트 - 유저 없음
        data = {
            'content': 'test content',
            'lodging_review': 1,
            'user': 100,
        }
        response = self.client.post(
            '/lodging/review/1/comment/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 400)
        print('숙소 리뷰 댓글 생성 테스트 - End')

        print('숙소 리뷰 댓글 수정 테스트 - Begin')
        # 숙소 리뷰 댓글 수정 테스트 - 인증O
        data = {
            'content': 'test content',
            'lodging_review': 1,
            'user': 1,
        }
        response = self.client.patch(
            '/lodging/review/1/comment/1/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 200)

        #숙소 리뷰 댓글 수정 테스트 - 숙소 리뷰 없음
        data = {
            'content': 'test content',
            'lodging_review': 100,
            'user': 1,
        }
        response = self.client.patch(
            '/lodging/review/100/comment/1/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 400)

        #숙소 리뷰 댓글 수정 테스트 - 유저 없음
        data = {
            'content': 'test content',
            'lodging_review': 1,
            'user': 100,
        }
        response = self.client.patch(
            '/lodging/review/1/comment/1/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 400)

        #숙소 리뷰 댓글 수정 테스트 - 댓글 없음
        data = {
            'content': 'test content',
            'lodging_review': 1,
            'user': 1,
        }
        response = self.client.patch(
            '/lodging/review/1/comment/100/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 404)
        print('숙소 리뷰 댓글 수정 테스트 - End')

        print('숙소 리뷰 댓글 리스트 테스트 - Begin')
        #숙소 리뷰 댓글 리스트 테스트 - 인증O
        data = {
            'content': 'test content',
            'lodging_review': 1,
            'user': 1,
        }
        response = self.client.get(
            '/lodging/review/1/comment/', 
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        print('숙소 리뷰 댓글 리스트 테스트 - End')

        print('숙소 리뷰 댓글 삭제 테스트 - Begin')
        #숙소 리뷰 댓글 삭제 테스트 - 인증O
        response = self.client.delete(
            '/lodging/review/1/comment/1/', 
            format='json',
        )
        self.assertEqual(response.status_code, 204)
        print('숙소 리뷰 댓글 삭제 테스트 - End')