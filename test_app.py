import pytest
import app as trail_file
import tempfile
import json


@pytest.fixture(scope='function')
def client():
    trail_file.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    trail_file.app.config['TESTING'] = True
    client = trail_file.app.test_client()

    with trail_file.app.app_context():
        trail_file.db.create_all()

    yield client


class TestUsers(object):
    @pytest.mark.users
    def test_register_user_empty(self, client):
        response = client.post('/register')
        response_data = json.loads(response.data)

        assert response_data['status'] == 'error'
        assert response_data['message'] == 'Make sure all form fields have been filled out'

    def test_register_user(self, client):
        response = client.post('/register', json={
            'username': 'B',
            'email': 'D',
            'password': "666",
            'confirmPassword': "666"
        })
        response_data = json.loads(response.data)
        assert response_data['id'] == 1
        assert response_data['username'] == 'B'

        with trail_file.app.app_context():
            user1 = trail_file.db.session.query(
                trail_file.Users).one().username
            email1 = trail_file.db.session.query(trail_file.Users).one().email
            saved_trails = trail_file.db.session.query(
                trail_file.Users).one().num_saved_trails
            id1 = trail_file.db.session.query(
                trail_file.Users).one().id

            assert user1 == 'B'
            assert email1 == 'D'
            assert saved_trails == 0
            assert id1 == 1

        with trail_file.app.app_context():
            id_1 = trail_file.db.session.query(
                trail_file.Login).one().id
            username_1 = trail_file.db.session.query(
                trail_file.Login).one().parent_username
            parent_1 = trail_file.db.session.query(
                trail_file.Login).one().parent_id

            assert id_1 == 1
            assert username_1 == 'B'
            assert parent_1 == 1

    def test_register_pre_existing(self, client):
        response = client.post('/register', json={
            'username': 'B',
            'email': 'D',
            'password': "666",
            'confirmPassword': "666"
        })
        response_data = json.loads(response.data)

        assert response_data['status'] == 'error'
        assert response_data['message'] == 'Username already exists'

    def test_register_passwords_dont_match(self, client):
        response = client.post('/register', json={
            'username': 'G',
            'email': 'E',
            'password': "666",
            'confirmPassword': "6667"
        })
        response_data = json.loads(response.data)

        assert response_data['status'] == 'error'
        assert response_data['message'] == 'Passwords dont match'

    def test_successful_signin(self, client):
        response = client.post('/signin', json={
            'username': 'B',
            'password': "666",
        })
        response_data = json.loads(response.data)
        assert response_data['id'] == 1
        assert response_data['username'] == 'B'

    def test_NON_successful_signin_password(self, client):
        response = client.post('/signin', json={
            'username': 'B',
            'password': "66",
        })
        response_data = json.loads(response.data)
        assert response_data['id'] == None
        assert response_data['username'] == None
        assert response_data['status'] == 'error'
        assert response_data['message'] == 'Password is incorrect'

    def test_NON_successful_signin_username(self, client):
        response = client.post('/signin', json={
            'username': 'BB',
            'password': "66",
        })
        response_data = json.loads(response.data)
        assert response_data['id'] == None
        assert response_data['username'] == None
        assert response_data['status'] == 'error'
        assert response_data['message'] == 'No matching user in database'

    def test_delete_user_from_db(self, client):
        response = client.post('/delete-user', json={
            'userId': '1',
        })
        response_data = json.loads(response.data)
        assert response_data['status'] == 1

    def test_delete_no_user_from_db(self, client):
        response = client.post('/delete-user', json={
        })
        response_data = json.loads(response.data)
        assert response_data['status'] == 0

    def test_delete_wrong_user_from_db(self, client):
        response = client.post('/delete-user', json={
            'userId': '10',
        })
        response_data = json.loads(response.data)
        assert response_data['status'] == 0


class TestTrails(object):
    @pytest.mark.trails
    def test_add_trails_to_user(self, client):
        response = client.post('/save-trail', json={
            'userId': 1,
            'trailId': '55',
            'trailData': 'stringofdata'
        })
        response_data = json.loads(response.data)
        assert response_data['trail'] == 55

        response = client.post('/save-trail', json={
            'userId': 1,
            'trailId': '99',
            'trailData': 'stringofdata2'
        })
        response_data = json.loads(response.data)
        assert response_data['trail'] == 99

        response = client.post('/save-trail', json={
            'userId': 11,
            'trailId': '929',
            'trailData': 'stringofdata2'
        })
        response_data = json.loads(response.data)
        assert response_data['trail'] == 929

    def test_load_trails(self, client):
        response = client.post('/load-trails', json={
            'userId': 1
        })
        response_data = json.loads(response.data)
        assert len(response_data['trails']) == 2

        response = client.post('/load-trails', json={
            'userId': 11
        })
        response_data = json.loads(response.data)
        assert len(response_data['trails']) == 1

        response = client.post('/load-trails', json={
            'userId': 111
        })
        response_data = json.loads(response.data)
        assert len(response_data['trails']) == 0

    def test_delete_trail_errors(self, client):
        response = client.post('/delete-trail', json={
            'userId': 1})
        response_data = json.loads(response.data)
        assert response_data['message'] == 'Missing arguments'

        response = client.post('/delete-trail', json={
            'trailId': 1})
        response_data = json.loads(response.data)
        assert response_data['message'] == 'Missing arguments'

        response = client.post('/delete-trail', json={
            'userId': 1,
            'trailId': 1})
        response_data = json.loads(response.data)
        assert response_data['status'] == 0

    def test_delete_trail_success(self, client):

        response = client.post('/delete-trail', json={
            'userId': 11,
            'trailId': 929})
        response_data = json.loads(response.data)
        assert response_data['status'] == 1

        response = client.post('/load-trails', json={
            'userId': 11
        })
        response_data = json.loads(response.data)
        assert len(response_data['trails']) == 0
