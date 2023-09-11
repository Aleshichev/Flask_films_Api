from flask import Flask
from flask_restful import Api
import config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Flask tutorial'
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

from src import models
from src.Resources.films import FilmListApi
from src.Resources.actors import ActorListApi
from src.Resources.auth import AuthRegister, AuthLogin
from src.Resources.populate_db import PopulateDB, PopulateDBThreaded, PopulateDBThreadPoolExecutor

api.add_resource(FilmListApi, '/films', '/films/<uuid>', strict_slashes=False)
api.add_resource(ActorListApi, '/actors', '/actors/<id>', strict_slashes=False)
api.add_resource(AuthRegister, '/register', strict_slashes=False)
api.add_resource(AuthLogin, '/login', strict_slashes=False)
api.add_resource(PopulateDB, '/populate_db', strict_slashes=False)
api.add_resource(PopulateDBThreaded, '/populate_db_threaded', strict_slashes=False)
api.add_resource(PopulateDBThreadPoolExecutor, '/populate_db_executor', strict_slashes=False)

