from flask import request
from marshmallow import ValidationError
from src import db
from flask_restful import Resource
from src.Resources.auth import token_required
from src.models import Film
from src.schemas.films import FilmSchema
from src.services.film_service import FilmService
from sqlalchemy.orm import selectinload

class FilmListApi(Resource):
    film_schema = FilmSchema()

    # @token_required
    def get(self, uuid=None):
        if not uuid:
            # films = db.session.query(Film).all()
            films = FilmService.fetch_all_films(db.session).options(
                selectinload(Film.actors)
            ).all()
            return self.film_schema.dump(films, many=True), 200
        # film = db.session.query(Film).filter_by(uuid=uuid).first()
        film = FilmService.fetch_film_by_uuid(db.session, uuid)

        if not film:
            return 'No film', 404


        return self.film_schema.dump(film), 200

    @token_required
    def post(self):
        try:
            film = self.film_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 201

    @token_required
    def put(self, uuid):

        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return "No Film", 404
        try:
            film = self.film_schema.load(request.json, instance=film, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 200

    @token_required
    def patch(self, uuid):

        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return "No Film", 404
        try:
            film = self.film_schema.load(request.json, instance=film, partial=True, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400

        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 200

    @token_required
    def delete(self, uuid):
        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return "", 404
        db.session.delete(film)
        db.session.commit()
        return '', 204
