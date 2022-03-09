from flask import Flask, Blueprint
from flask_restx import Api
from flask_migrate import Migrate
from app.resources import *

from app.db import init_db


def init_app():
    app = Flask(__name__)

    blueprint = Blueprint('api', __name__, url_prefix='/api/')
    app.register_blueprint(blueprint)

    migrate = Migrate()
    migrate.init_app(app)

    return app


def init_api():
    api = Api(
        app,
        title='Social Network',
        description='The basic model of social network',
        version='1.0',
        prefix='/api/',
        ordered=True,
    )

    return api

app = init_app()
api = init_api()
db = init_db(app)


if __name__ == "__main__":
    # app = init_app()
    # api = init_api()
    # db = init_db(app)
    Login()
    Logout()
    SignUp()



    app.run(host="0.0.0.0", port=5001)
