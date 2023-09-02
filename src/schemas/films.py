from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,  auto_field
from marshmallow_sqlalchemy.fields import Nested
from src.models import Film

class FilmSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Film
        exclude = ['id']
        load_instance = True
        include_fk = True

    title = auto_field()
    release_date = auto_field()
    uuid = auto_field()
    description = auto_field()
    distributed_by = auto_field()
    length = auto_field()
    rating = auto_field()
    actors = Nested('ActorSchema', many=True, exclude=('films',))