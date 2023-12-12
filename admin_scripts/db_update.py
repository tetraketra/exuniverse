from exuniverse.app import flask_app
from exuniverse.db import *

with flask_app.app_context() as app_context:
    flask_db.create_all()