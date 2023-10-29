import os

from flask import Flask
from flask_restful import Resource, Api
from flask_login import LoginManager

from . import db
from . import os_addons


## APP ## TODO: config files, testing, actually secret secrets
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='CED0567CB8B29657FE1EB8132FAE5707FCD4C67DBF744CDDED5BDE7C0BD49594',
    DATABASE=os.path.join(app.instance_path, 'app.db'),
)

os_addons.ensure_dir(app.instance_path)

db.init_app(app)

## API ## TODO: all of this lmao
api = Api(app)

## LOGINMANAGER ## TODO: all of this lmao
login_manager = LoginManager()
login_manager.init_app(app)

## RUN ##
if __name__ == "main":
    app.run(debug = True) # FIXME: Never deploy with `debug = True`!