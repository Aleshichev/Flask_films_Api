import http
from src import app

class TestFilms:
    def test_get_films_with_db(self):
        client = app.test_client()
        resp = client.get('/films')

        assert resp.status_code == http.HTTPStatus.OK

if __name__ == '__main__':
    app.run()