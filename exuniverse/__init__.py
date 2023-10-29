import os

from flask import Flask
from flask_restful import Resource, Api
from flask_login import LoginManager

from . import db
from . import os_addons


def init_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping( # TODO: config files, actually secret secrets
        SECRET_KEY='CED0567CB8B29657FE1EB8132FAE5707FCD4C67DBF744CDDED5BDE7C0BD49594',
        DATABASE=os.path.join(app.instance_path, 'exuniverse.db'),
    )

    os_addons.ensure_dir(app.instance_path)

    db.link_to_app(app)
    
    return app


def init_login_manager(app: Flask) -> LoginManager:
    login_manager = LoginManager()
    login_manager.init_app(app)

    # TODO: all of this lmao

    return login_manager


def init_api(app: Flask) -> Api: 
    api = Api(app)

    # TODO: all of this lmao

    return api


def create_app() -> Flask:
    # This structure is borrowed from C conventions for 
    # maximum readability, separation, and clarity.
    
    app: Flask = init_app()
    login_manager: LoginManager = init_login_manager(app)
    api: Api = init_api(app)

    return app