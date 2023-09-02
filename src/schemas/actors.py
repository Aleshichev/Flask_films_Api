from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from src.models import Actor


class ActorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Actor
        load_instance = True
        include_fk = True

    name = auto_field()
    birthday = auto_field()
    is_active = auto_field()
    films = Nested('FilmSchema', many=True, exclude=('actors',))
