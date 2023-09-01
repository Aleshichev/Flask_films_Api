from flask import Flask
from flask_restful import Api
import config
from src.routes import Smoke, FilmListApi
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

api.add_resource(Smoke, '/smoke', strict_slashes=False)
api.add_resource(FilmListApi, '/films', '/films/<uuid>', strict_slashes=False)

from src import models