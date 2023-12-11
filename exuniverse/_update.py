from app import app
from db import *

with app.app_context() as app_context:
    db.create_all()