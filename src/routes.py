from flask import request
from marshmallow import ValidationError

from src import db
from flask_restful import Resource
from src.models import Film, Actor
from src.schemas.actors import ActorSchema
from src.schemas.films import FilmSchema

class FilmListApi(Resource):
    film_schema = FilmSchema()

    def get(self, uuid=None):

        if not uuid:
            films = db.session.query(Film).all()
            return self.film_schema.dump(films, many=True), 200
        film = db.session.query(Film).filter_by(uuid=uuid).first()

        if not film:
            return 'No film', 404
        return self.film_schema.dump(film), 200

    def post(self):
        try:
            film = self.film_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 201

    def put(self, uuid):

        film = db.session.query(Film).filter_by(uuid=uuid).first()
        if not film:
            return "No Film", 404
        try:
            film = self.film_schema.load(request.json, instance=film, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 200

    def patch(self, uuid):

        film = db.session.query(Film).filter_by(uuid=uuid).first()
        if not film:
            return "No Film", 404
        try:
            film = self.film_schema.load(request.json, instance=film, partial=True, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400

        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 200

    def delete(self, uuid):
        film = db.session.query(Film).filter_by(uuid=uuid).first()
        if not film:
            return "", 404
        db.session.delete(film)
        db.session.commit()
        return '', 204

class ActorListApi(Resource):
    actor_schema = ActorSchema()

    def get(self, id=None):

        if not id:
            actor = db.session.query(Actor).all()
            return self.actor_schema.dump(actor, many=True), 200
        actor = db.session.query(Actor).filter_by(id=id).first()

        if not actor:
            return 'No film', 404
        return self.actor_schema.dump(actor), 200

    def post(self):
        try:
            actor = self.actor_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(actor)
        db.session.commit()
        return self.actor_schema.dump(actor), 201

    def put(self, id):

        actor = db.session.query(Actor).filter_by(id=id).first()
        if not actor:
            return "No Film", 404
        try:
            actor = self.actor_schema.load(request.json, instance=actor, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(actor)
        db.session.commit()
        return self.actor_schema.dump(actor), 200

    def patch(self, id):

        actor = db.session.query(Actor).filter_by(id=id).first()
        if not actor:
            return "No Film", 404
        try:
            film = self.actor_schema.load(request.json, instance=actor, partial=True, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400

        db.session.add(actor)
        db.session.commit()
        return self.actor_schema.dump(actor), 200

    def delete(self, id):
        actor = db.session.query(Actor).filter_by(id=id).first()
        if not actor:
            return "", 404
        db.session.delete(actor)
        db.session.commit()
        return '', 204


