import hashlib
import sqlite3
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .db import query_db


@dataclass_json
@dataclass
class User():
    id: str
    username: str
    password_hashed: str
    password_salt: str
    email: str
    is_authenticated: bool
    is_active: bool
    is_anonymous: bool
    profile_name: str
    profile_about: str
    profile_pic_link: str

    @classmethod
    def get(cls, user_id: str, conn: sqlite3.Connection) -> 'User':
        d: dict = query_db(
            conn, 
            f"SELECT * FROM users WHERE id = {user_id}"
        )[0]
        return User(
            id=user_id, email=d['email'], username=d['username'],
            profile_name=d['profile_name'], profile_about=d['profile_about'],
            profile_pic_link=d['profile_pic_link'], is_active=d['is_active'],
            password_hashed=d['password'], password_salt=d['password_salt']
        )

    @classmethod
    def get_hashed_password(cls, password: str, password_salt: str) -> str:
        return hashlib.sha256(
            (password + password_salt + "twitchchat").encode('utf-8')
        ).hexdigest()

    def login(self, username: str, password: str) -> bool:
        p = User.get_hashed_password(password, self.password_salt)
        if self.username == username and self.password_hashed == p:
            self.is_authenticated = True
        return self.is_authenticated

    def logout(self) -> bool:
        self.is_authenticated = False
        return self.is_authenticated

    # necessary for flask-login
    def get_id(self) -> str:
        return str(self.id)