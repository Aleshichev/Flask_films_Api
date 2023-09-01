from flask_restful import Resource

def get_all_films():
    pass

def get_film_by_uuid(uuid:str) -> dict:
    films = get_all_films()
    film = list(filter(lambda f: f['id'] == uuid, films))
    return film[0] if film else {}

def create_film(film_json: dict):
    films = get_all_films()
    films.append(film_json)
    return films

class Smoke(Resource):
    def get(self):
        return {'message': 'ok'}, 200

class FilmListApi(Resource):
    def get(self, uuid=None):
        if not uuid:
            films = get_all_films()
        film = get_film_by_uuid(uuid)
        if not film:
            return '', 404
        return film, 200

    def post(self):
        pass
    def put(self):
        pass
    def patch(self):
        pass
    def delete(self):
        pass

class ActorListApi(Resource):
    def get(self, uuid=None):
        if not uuid:
            films = get_all_films()
        film = get_film_by_uuid(uuid)
        if not film:
            return '', 404
        return film, 200

    def post(self):
        pass
    def put(self):
        pass
    def patch(self):
        pass
    def delete(self):
        pass