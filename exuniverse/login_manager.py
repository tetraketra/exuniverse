import sqlite3
from flask_login import LoginManager

from .db import get_db
from .app import app
from .user import User


login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    conn: sqlite3.Connection = get_db()
    return User.get(conn, user_id)

login_manager.init_app(app)