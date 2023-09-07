import http
import json
from src import app, db
from dataclasses import dataclass
from unittest.mock import patch
from src.models import User
import pytest

# hide @token_required before start

@pytest.fixture(scope='function')
def cleanup_last_user():
    yield
    with app.app_context():
        last_user = User.query.order_by(User.id.desc()).first()
        if last_user:
                db.session.delete(last_user)
                db.session.commit()


@dataclass
class FakeUser:
    username = 'Fake User'
    email = 'User@ua.com'
    password = '9i8u7y6t'
    is_admin = True


class TestRegisterUser:


    def test_registration_user_with_db(self):
        client = app.test_client()
        data = {'username': 'Fake User',
                'email': 'User@ua.com',
                'password': '9i8u7y6t',
                'is_admin': True
                }
        resp = client.post('/register', data=json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json['username'] == 'Fake User'


    def test_registration_user_with_mock_db(self):
        with patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            client = app.test_client()
            data = {'username': 'Fake User',
                    'email': 'User@ua.com',
                    'password': '9i8u7y6t',
                    'is_admin': True
                    }
            resp = client.post('/register', data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()
            assert resp.status_code == http.HTTPStatus.CREATED



    def test_wrong_email_registration_user_with_db(self):
        client = app.test_client()
        data = {'username': 'Fake User',
                'email': 'User',
                'password': '9i8u7y6t',
                'is_admin': True
                }
        resp = client.post('/register', data=json.dumps(data), content_type='application/json')
        response_data = json.loads(resp.data.decode('utf-8'))
        expected_message = "{'email': ['Not a valid email address.']}"
        assert 'message' in response_data
        assert response_data['message'] == expected_message

    def test_wrong_email_user_with_mock_db(self):
        with patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            client = app.test_client()
            data = {'username': 'Fake User',
                    'email': 'User',
                    'password': '9i8u7y6t',
                    'is_admin': True
                }
            resp = client.post('/register', data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_not_called()
            mock_session_commit.assert_not_called()
            response_data = json.loads(resp.data.decode('utf-8'))
            expected_message = "{'email': ['Not a valid email address.']}"
            assert 'message' in response_data
            assert response_data['message'] == expected_message

    def test_wrong_password_registration_user_with_db(self):
        client = app.test_client()
        data = {'username': 'New User',
                'email': 'User@ua.com',
                'password': '234',
                'is_admin': True
                }
        resp = client.post('/register', data=json.dumps(data), content_type='application/json')
        response_data = json.loads(resp.data.decode('utf-8'))
        expected_message = "{'password': ['Password must be at least 8 characters long.']}"
        assert 'message' in response_data
        assert response_data['message'] == expected_message

    def test_wrong_password_user_with_mock_db(self):
        with patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            client = app.test_client()
            data = {'username': 'New User',
                    'email': 'User@ua.com',
                    'password': '234'
                }
            resp = client.post('/register', data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_not_called()
            mock_session_commit.assert_not_called()
            response_data = json.loads(resp.data.decode('utf-8'))
            expected_message = "{'password': ['Password must be at least 8 characters long.']}"
            assert 'message' in response_data
            assert response_data['message'] == expected_message


    def test_exist_registration_user_with_db(self):
        client = app.test_client()
        data = {'username': 'Fake User',
                'email': 'User@ua.com',
                'password': '9i8u7y6t',
                'is_admin': True
                }
        resp = client.post('/register', data=json.dumps(data), content_type='application/json')
        response_data = json.loads(resp.data.decode('utf-8'))
        expected_message = "Such user exists"
        assert 'message' in response_data
        assert response_data['message'] == expected_message
        assert resp.status_code == http.HTTPStatus.CONFLICT

    def test_exist_registration_user_with_mock_db(self, cleanup_last_user):
        with patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit, \
                patch('src.db.session.query', autospec=True) as mocked_query:
            client = app.test_client()
            data = {'username': 'Fake User',
                'email': 'User@uu.com',
                'password': '9i8u7y6t',
                'is_admin': True
                }
            mocked_query.return_value = FakeUser()
            resp = client.post('/register', data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()
            response_data = json.loads(resp.data.decode('utf-8'))
            print(mocked_query.return_value.username)
            assert mocked_query.return_value.username == response_data['username']

if __name__ == '__main__':
    app.run()