import unittest
import json
from app import create_app
from models.models import User, Post
from datetime import datetime
from werkzeug.security import generate_password_hash
from mongoengine import connect, disconnect


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost')
        self.db_setUp()
        self.client = self.app.test_client()

    def tearDown(self):
        disconnect()

    def db_setUp(self):
        """테스트하기 위해 db에 기본적으로 세팅되어야할 데이터들"""
        authorized_username = "test1"
        authorized_password = "password"
        unauthorized_username = "test2"
        unauthorized_user_password = "password"
        authorized_user = User(name=authorized_username, password=generate_password_hash(authorized_password),
                               signup_date=datetime.now()).save()
        User(name=unauthorized_username, password=generate_password_hash(unauthorized_user_password),
             signup_date=datetime.now()).save()
        for i in range(20):
            post = Post(title="subject{}".format(i), content="content", create_date=datetime.now(),
                        user=str(authorized_user.id), hits=0).save()
        global post_id
        post_id = str(post.id)

    def get_authorized_access_token(self):
        """권한있는 게시자의 access_token을 get반환하는 함수"""
        test_data = {"name": "test1", "password": "password"}
        rv2 = self.client.post('/auth/login/', data=json.dumps(test_data), content_type='application/json')
        json_data = rv2.get_json()
        access_token = json_data["access_token"]
        return access_token

    def get_unauthorized_access_token(self):
        """권한없는 게시자의 access_token을 반환하는 함수"""
        test_data = {"name": "test2", "password": "password"}
        rv2 = self.client.post('/auth/login/', data=json.dumps(test_data), content_type='application/json')
        json_data = rv2.get_json()
        access_token = json_data["access_token"]
        return access_token

    def test_get_post_list(self):
        """get_post_list시 200상태코드를 반환"""
        url = '/posts'
        response = self.client.get(url)
        assert 200 == response.status_code

    def test_detail_api_with_exited_post_id(self):
        """존재하는 게시글 식별자로 get요청시 200상태코드반환"""
        url = '/posts/{}'.format(post_id)
        response = self.client.get(url)
        assert 200 == response.status_code

    def test_detail_api_with_not_exited_post_id(self):
        """존재하지 않는 게시글 식별자로 get요청시 404상태코드 반환"""
        url = '/posts/1000/'
        response = self.client.get(url)
        assert 404 == response.status_code

    def test_post_with_access_token(self):
        """로그인된채로 글을 post요청시 201상태코드 반환"""
        access_token = self.get_authorized_access_token()
        test_data2 = {"title": "test3", "content": "test", "tags": ['test']}
        rv = self.client.post('/create', data=json.dumps(test_data2), content_type='application/json',
                              headers={"Authorization": "Bearer {}".format(access_token)})

        assert 201 == rv.status_code

    def test_post_without_access_token(self):
        """로그인 안된채로 글을 post요청시 401상태코드 반환"""
        test_data2 = {"title": "test3", "content": "test"}
        rv = self.client.post('/create', data=json.dumps(test_data2), content_type='application/json')

        assert 401 == rv.status_code

    def test_modify_with_authrorized_user(self):
        """권한있는 유저가 수정요청시 200 상태코드를 반환"""
        access_token = self.get_authorized_access_token()
        test_data2 = {"title": "modify", "content": "test"}
        rv = self.client.patch('/posts/{}'.format(post_id), data=json.dumps(test_data2),
                               content_type='application/json',
                               headers={"Authorization": "Bearer {}".format(access_token)})
        assert 200 == rv.status_code

    def test_modify_with_unauthrorized_user(self):
        """권한없는 유저가 수정요청시 401 상태코드를 반환"""
        access_token = self.get_unauthorized_access_token()
        test_data2 = {"title": "modify", "content": "test"}
        rv = self.client.patch('/posts/{}'.format(post_id), data=json.dumps(test_data2),
                               content_type='application/json',
                               headers={"Authorization": "Bearer {}".format(access_token)})
        assert 401 == rv.status_code

    def test_modify_not_existed_post(self):
        """존재하지 않는 게시글에 대한 수정 요청시 404 상태코드를 반환"""
        access_token = self.get_authorized_access_token()
        test_data2 = {"title": "modify", "content": "test", 'tags': ["test"]}
        self.client.delete('/posts/{}'.format(post_id), headers={"Authorization": "Bearer {}".format(access_token)})
        rv = self.client.patch('/posts/{}'.format(post_id), data=json.dumps(test_data2),
                               content_type='application/json',
                               headers={"Authorization": "Bearer {}".format(access_token)})
        assert 404 == rv.status_code

    def test_delete_with_authorized_user(self):
        """권한있는 유저가 삭제요청시 204 상태코드를 반환"""
        access_token = self.get_authorized_access_token()
        rv = self.client.delete('/posts/{}'.format(post_id),
                                headers={"Authorization": "Bearer {}".format(access_token)})
        assert 204 == rv.status_code

    def test_delete_with_unauthorized_user(self):
        """권한없는 유저가 삭제요청시 401 상태코드를 반환"""
        access_token = self.get_unauthorized_access_token()
        rv = self.client.delete('/posts/{}'.format(post_id),
                                headers={"Authorization": "Bearer {}".format(access_token)})
        assert 401 == rv.status_code

    def test_delete_with_not_exist_post(self):
        """존재하지 않는 게시글에 대한 삭제요청시 404 상태코드를 반환"""
        access_token = self.get_authorized_access_token()
        rv = self.client.delete('/delete/1000', headers={"Authorization": "Bearer {}".format(access_token)})
        assert 404 == rv.status_code


if __name__ == '__main__':
    unittest.main()
