import os
import binascii

import sqlite3
from flask import Response, request
from marshmallow import Schema, fields
from flask_restful import Resource, Api, reqparse, abort
from werkzeug.exceptions import BadRequest

from .app import app
from .db import get_db
from .user import User


api = Api(app)

class RegisterUser_InputSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.String(required=True)
class RegisterUser(Resource):    
    def post(self) -> dict:
        args = request.get_json(force=True)
        if er := RegisterUser_InputSchema().validate(request.json):
            abort(400, message=f"Argument parsing failed: {er}")
        
        conn: sqlite3.Connection = get_db()
        curs: sqlite3.Cursor = conn.cursor()
        salt: str = binascii.b2a_hex(os.urandom(5)).decode('utf-8')

        try:
            curs.execute(f"""
                INSERT INTO users(username, password, password_salt, email)
                VALUES("{args['username']}", "{User.get_hashed_password(
                args['password'], salt)}", "{salt}", "{args['email']}")
            """)
            conn.commit()
            return {'id':curs.lastrowid}

        except sqlite3.Error as er:
            if er.sqlite_errorname == "SQLITE_CONSTRAINT_UNIQUE":
                abort(409, message=f"A user with that username already exists.")
            
            abort(400, message=f"Unhandled SQLite3 error: {er.sqlite_errorname}")
            

api.add_resource(RegisterUser, '/user/register')