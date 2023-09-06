from src.models import Actor


class ActorService:

    @staticmethod
    def fetch_all_actors(session):
        return session.query(Actor)

    @classmethod
    def fetch_actor_by_id(cls, session, id):
        return cls.fetch_all_actors(session).filter_by(
            id=id
        ).first()