from flask import request
from marshmallow import ValidationError

from src import db
from flask_restful import Resource
from src.models import Actor
from src.schemas.actors import ActorSchema


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


