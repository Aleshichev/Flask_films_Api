import http
import json
from src import app
from dataclasses import dataclass
from unittest.mock import patch
from src.models import Actor
from src import db

@dataclass
class FakeActor:
    name = 'Fake Actor'
    birthday = '2002-12-03'
    is_active = 'True'


class TestActors:


    def last_id(self):
        with app.app_context():
            last_actor = db.session.query(Actor).order_by(Actor.id.desc()).first()
            last_actor_id = last_actor.id
        return last_actor_id

    id = []

    def test_get_actors_with_db(self):
        client = app.test_client()
        resp = client.get('/actors')

        assert resp.status_code == http.HTTPStatus.OK

    @patch('src.services.actor_services.ActorService.fetch_all_actors', autospec=True)
    def test_get_actors_mock_db(self, mock_db_call):
        client = app.test_client()
        resp = client.get('/actors')
        mock_db_call.assert_called_once()
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json) == 0


    def test_create_actor_with_db(self):
        client = app.test_client()
        data = {'name': 'New Actor',
                'birthday': '2022-12-03',
                'is_active': 'True'}
        resp = client.post('/actors', data=json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json['name'] == 'New Actor'
        self.id.append(resp.json['id'])

    def test_create_actor_with_mock_db(self):
        with patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            client = app.test_client()
            data = {'name': 'New Actor',
                    'birthday': '2022-12-03',
                    'is_active': 'True'}
            resp = client.post('/actors', data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_update_actor_with_db(self):
        client = app.test_client()
        url = f'/actors/{self.last_id()}'
        data = {'name': 'Update Actor',
                'birthday': '2022-12-03',
                'is_active': 'True'}
        resp = client.put(url, data=json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json['name'] == 'Update Actor'

    def test_update_actor_with_mock_db(self):
        with patch('src.services.actor_services.ActorService.fetch_actor_by_id') as mocked_query, \
                patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            mocked_query.return_value = FakeActor()
            client = app.test_client()
            url = f'/actors/1'
            data = {
                'name': 'Update Actor',
                'birthday': '2022-12-03',
                'is_active': 'True'
            }
            resp = client.put(url, data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()
            assert resp.status_code == http.HTTPStatus.OK

    def test_patch_actor_with_db(self):
        client = app.test_client()
        with app.app_context():
            last_actor = db.session.query(Actor).order_by(Actor.id.desc()).first()
            last_actor_id = last_actor.id
        url = f'/actors/{self.last_id()}'
        data = {
            'name': 'Patch Actor'
                }
        resp = client.patch(url, data=json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json['name'] == 'Patch Actor'

    def test_patch_actor_with_mock_db(self):
        with patch('src.services.actor_services.ActorService.fetch_actor_by_id') as mocked_query, \
                patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            mocked_query.return_value = FakeActor()
            client = app.test_client()
            url = f'/actors/1'
            data = {
                'birthday': '2002-12-03',
            }
            resp = client.patch(url, data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()
            assert resp.status_code == http.HTTPStatus.OK

    def test_delete_actor_with_db(self):
        client = app.test_client()
        url = f'/actors/{self.last_id()}'
        resp = client.delete(url)
        assert resp.status_code == http.HTTPStatus.NO_CONTENT

if __name__ == '__main__':
    app.run()