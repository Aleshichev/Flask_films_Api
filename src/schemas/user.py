from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.validate import Email
from src.models import User
from marshmallow import fields, ValidationError

def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not any(char.isdigit() for char in password):
        raise ValidationError("Password must contain at least one digit.")


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('id',)
        load_instance = True
        load_only = ('password',)

    email = fields.Str(required=True, validate=Email())
    password = fields.Str(required=True, validate=validate_password)
