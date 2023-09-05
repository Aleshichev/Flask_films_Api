import http
import json
from src import app
from unittest.mock import patch

class TestFilms:

    # def test_get_films_with_db(self):
    #     client = app.test_client()
    #     resp = client.get('/films')
    #
    #     assert resp.status_code == http.HTTPStatus.OK
    #
    # @patch('src.services.film_service.FilmService.fetch_all_films', autospec=True)
    # def test_get_films_mock_db(self, mock_db_call):
    #     client = app.test_client()
    #     resp = client.get('/films')
    #     mock_db_call.assert_called_once()
    #     assert resp.status_code == http.HTTPStatus.OK
    #     assert len(resp.json) == 0


    # def test_create_film_with_db(self):
    #     client = app.test_client()
    #     data = {
    #         'title': 'Test Title',
    #         'distributed_by': 'Test Company',
    #         'release_date': '2010-04-01',
    #         'description': '',
    #         'length': 100,
    #         'rating': 8.0
    #     }
    #     resp = client.post('/films', data=json.dumps(data), content_type='application/json')
    #     assert resp.status_code == http.HTTPStatus.CREATED
    #     assert resp.json['title'] == 'Test Title'
        # self.uuid.append(resp.json['uuid'])

    def test_create_film_with_mock_db(self):
        with patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            client = app.test_client()
            data = {
                'title': 'Test Title',
                'distributed_by': 'Test Company',
                'release_date': '2010-04-01',
                'description': '',
                'length': 100,
                'rating': 8.0
            }
            resp = client.post('/films', data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

if __name__ == '__main__':
    app.run()