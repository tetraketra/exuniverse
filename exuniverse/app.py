import os

import sqlite3
from flask import Flask
from flask_login import LoginManager

from .db import link_db_to_app, get_db
from .extras import os_extras


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping( # TODO: config files, actually secret secrets
    SECRET_KEY='CED0567CB8B29657FE1EB8132FAE5707FCD4C67DBF744CDDED5BDE7C0BD49594',
    DATABASE=os.path.join(app.instance_path, 'exuniverse.db'),
)

os_extras.ensure_dir(app.instance_path)
link_db_to_app(app)