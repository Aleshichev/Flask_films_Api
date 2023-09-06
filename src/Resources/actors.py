from flask import request
from marshmallow import ValidationError
from src import db
from flask_restful import Resource
from src.models import Actor
from src.schemas.actors import ActorSchema
from sqlalchemy.orm import selectinload
from src.services.actor_services import ActorService
from .auth import token_required


class ActorListApi(Resource):
    actor_schema = ActorSchema()

    # @token_required
    def get(self, id=None):

        if not id:
            # actor = db.session.query(Actor).all()
            actors = ActorService.fetch_all_actors(db.session).options(
                selectinload(Actor.films)
            ).all()
            return self.actor_schema.dump(actors, many=True), 200
        # actor = db.session.query(Actor).filter_by(id=id).first()
        actor = ActorService.fetch_actor_by_id(db.session, id)


        if not actor:
            return 'No film', 404
        return self.actor_schema.dump(actor), 200

    # @token_required
    def post(self):
        try:
            actor = self.actor_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(actor)
        db.session.commit()
        return self.actor_schema.dump(actor), 201

    # @token_required
    def put(self, id):

        actor = ActorService.fetch_actor_by_id(db.session, id)
        if not actor:
            return "No Film", 404
        try:
            actor = self.actor_schema.load(request.json, instance=actor, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(actor)
        db.session.commit()
        return self.actor_schema.dump(actor), 200

    # @token_required
    def patch(self, id):

        actor = ActorService.fetch_actor_by_id(db.session, id)
        if not actor:
            return "No Film", 404
        try:
            film = self.actor_schema.load(request.json, instance=actor, partial=True, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400

        db.session.add(actor)
        db.session.commit()
        return self.actor_schema.dump(actor), 200

    # @token_required
    def delete(self, id):

        actor = ActorService.fetch_actor_by_id(db.session, id)
        if not actor:
            return "", 404
        db.session.delete(actor)
        db.session.commit()
        return '', 204


