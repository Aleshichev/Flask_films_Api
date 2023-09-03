import pathlib

BASE_DIR = pathlib.Path(__file__).parent

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / "data" / "db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICSTIONS = False
    SECRET_KEY = '425frty8s466g'
