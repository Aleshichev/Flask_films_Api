import datetime
from functools import wraps

import jwt
from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from src import db, app
from src.models import User
from src.schemas.user import UserSchema


class AuthRegister(Resource):
    user_schema = UserSchema()

    def post(self):
        try:
            user = self.user_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {"message": str(e)}
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"message": "Such user exists"}, 409
        return self.user_schema.dump(user), 201


class AuthLogin(Resource):
    def post(self):

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {"message": "Username and password are required"}, 400

        user = db.session.query(User).filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return {"message": "Invalid credentials"}, 401

        token = jwt.encode(
            {
                "user_id": user.uuid,
                "exp": datetime.datetime.now() + datetime.timedelta(minutes=5)
            }, app.config['SECRET_KEY']
        )
        return jsonify(
            {
                "token": token
            }
        )


def token_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        token = request.headers.get('Authorization', '')
        if token.startswith("Bearer "):
            token = token[len("Bearer "):]
        if not token:
            return "No Token", 401
        try:
            uuid = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")['user_id']
        except (KeyError, jwt.ExpiredSignatureError):
            return "", 401
        except jwt.DecodeError as e:
            return (f"Error decoding token: {str(e)}"), 401
        user = db.session.query(User).filter_by(uuid=uuid).first()
        if not user:
            return "", 401
        return func(self, *args, **kwargs)

    return wrapper
