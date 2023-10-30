import os
import binascii

import sqlite3
from collections import defaultdict
from flask import request, Request
from flask_restful import Resource, Api, abort
from flask_login import login_user, logout_user, login_required
from marshmallow import Schema, fields
from urllib.parse import urlparse, ParseResult

from .app import app
from .db import get_db, query_db
from .user import User
from .login_manager import login_manager


api = Api(app)

def url_has_allowed_host_and_scheme(
    url: str, allowed_hosts: str | set[str], require_https: bool = True
) -> bool:
    """
    Use this to validate the `next` url property on a redirection (such as
    after login) to protect against [open redirection](https://portswigger.net/kb/issues/00500100_open-redirection-reflected).
    """
    
    if url is not None:
        url = url.strip()
    if not url:
        return False
    if url.startswith('///'):
        return False
    if allowed_hosts is None:
        allowed_hosts = set()
    elif isinstance(allowed_hosts, str):
        allowed_hosts = {allowed_hosts}
        
    try:
        url_info: ParseResult = urlparse(url)
        if not url_info.netloc and url_info.scheme:
            return False
        if not url_info.scheme in (['https'] if require_https else ['http', 'https']):
            return False
        if not url_info.hostname in allowed_hosts:
            return False
    except:
        return False

    return True


def api_call_setup(
    request: Request, schema: Schema
) -> tuple[dict, sqlite3.Connection]:
    """
    Run this at the beginning of each Flask-RESTful GET/PUT/POST method to
    fetch the JSON input arguments and db connection object `conn`. 
    """

    conn: sqlite3.Connection = get_db()
    args = defaultdict(lambda: None, request.get_json(force=True))
    if er := schema().validate(request.json):
        abort(400, message=f"Argument parsing failed: {er}")
    
    return args, conn

    
class RegisterUser_InputSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    email    = fields.String(required=True)
class RegisterUser(Resource):    
    def post(self):
        args, conn = api_call_setup(request=request, schema=RegisterUser_InputSchema)
        salt: str = binascii.b2a_hex(os.urandom(5)).decode('utf-8')
        sql: str = f"""
            INSERT INTO users (
                username, email,
                password, password_salt
            )
            VALUES (
                ?, ?,
                ?, ?
            );
        """
        vals = (
            args['username'], args['email'],
            User.get_hashed_password(args['password'], salt), salt
        )

        try:
            return { 'id':str(query_db(conn=conn, sql=sql, vals=vals, method="commit")) } # SUCCESS
        
        except sqlite3.Error as er:
            if er.sqlite_errorname == "SQLITE_CONSTRAINT_UNIQUE":
                abort(409, message=f"A user with that username already exists.")
            
            abort(400, message=f"Unhandled SQLite3 error: {er.sqlite_errorname}")


class GetCard_InputSchema(Schema):
    id                      = fields.Integer(required=True)
class PostPutCard_InputSchema(Schema):
    # REQUIRED: name, template_type_id, template_subtype_id, template_attribute_id
    name                    = fields.String (required=True)
    treated_as              = fields.String (required=False)
    effect                  = fields.String (required=False)
    pic                     = fields.String (required=False)
    template_type_id        = fields.Integer(required=True)
    template_subtype_id     = fields.Integer(required=True)
    template_attribute_id   = fields.Integer(required=True)
    monster_atk             = fields.Integer(required=False)
    monster_def             = fields.Integer(required=False)
    monster_is_gemini       = fields.Integer(required=False)
    monster_is_spirit       = fields.Integer(required=False)
    monster_is_toon         = fields.Integer(required=False)
    monster_is_tuner        = fields.Integer(required=False)
    monster_is_union        = fields.Integer(required=False)
    monster_is_flip         = fields.Integer(required=False)
    pendulum_scale          = fields.Integer(required=False)
    pendulum_effect         = fields.String (required=False)
    link_arrows             = fields.String (required=False)
    ocg                     = fields.Integer(required=False)
    ocg_date                = fields.Integer(required=False)
    ocg_limit               = fields.Integer(required=False)
    tcg                     = fields.Integer(required=False)
    tcg_date                = fields.Integer(required=False)
    tcg_limit               = fields.Integer(required=False)
    exu_limit               = fields.Integer(required=False)
    created_by_id           = fields.Integer(required=False)
class Card(Resource):
    def get(self):
        args, conn = api_call_setup(request=request, schema=GetCard_InputSchema)
        sql: str = f""" SELECT * FROM cards WHERE id = {args['id']}; """
        
        try:
            return dict( query_db(conn, sql)[0] ) # SUCCESS
        
        except:
            abort(404, message=f"No card found with id={args['id']}")

        
    def post(self):
        args, conn = api_call_setup(request=request, schema=PostPutCard_InputSchema)
        curs: sqlite3.Cursor = conn.cursor()
        sql: str = f""" 
            INSERT INTO cards (
                name, treated_as, effect, pic,
                template_type_id, template_subtype_id, template_attribute_id,
                monster_atk, monster_def, monster_type_id,
                monster_is_gemini, monster_is_spirit, monster_is_toon, 
                monster_is_tuner, monster_is_union, monster_is_flip,
                pendulum_scale, pendulum_effect,
                link_arrows,
                ocg, ocg_date, ocg_limit,
                tcg, tcg_date, tcg_limit,
                exu_limit,
                created_by_id
            )
            VALUES (
                ?, ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?,
                ?, ?,
                ?,
                ?, ?, ?,
                ?, ?, ?,
                ?,
                ?
            );
        """
        vals = (
            args['name'], args['treated_as'], args['effect'], args['pic'],
            args['template_type_id'], args['template_subtype_id'], args['template_attribute_id'],
            args['monster_atk'], args['monster_def'], args['monster_type_id'],
            args['monster_is_gemini'], args['monster_is_spirit'], args['monster_is_toon'],
            args['monster_is_tuner'], args['monster_is_union'], args['monster_is_flip'],
            args['pendulum_scale'], args['pendulum_effect'],
            args['link_arrows'],
            args['ocg'], args['ocg_date'], args['ocg_limit'],
            args['tcg'], args['tcg_date'], args['tcg_limit'],
            args['exu_limit'],
            args['created_by_id']
        )
        
        try:
            return { 'id':query_db(conn=conn, sql=sql, vals=vals, method="commit") } # SUCCESS

        except sqlite3.Error as er:
            if er.sqlite_errorname == "SQLITE_CONSTRAINT_UNIQUE":
                abort(409, message=f"A card with that name already exists.")

            abort(400, message=f"Unhandled SQLite3 error: {er.sqlite_errorname}")

        
    def put(self):
        ...


# # TODO: ACTUAL WEBPAGE STUFF INSTEAD OF API. DO NOT USE AUTH FOR API REQUESTS!
# # FIXME: Adjust to match https://flask-login.readthedocs.io/en/latest/#configuring-your-application
# #        once login form is ready.
# class LoginUser_InputSchema(Schema):
#     username = fields.String(required=True)
#     password = fields.String(required=True)
# class LoginUser(Resource):
#     def post(self):
#         args = request.get_json(force=True)
#         if er := LoginUser_InputSchema().validate(request.json):
#             abort(400, message=f"Argument parsing failed: {er}")
#
#         conn: sqlite3.Connection = get_db()
#         id: str = query_db(
#             conn, f"SELECT id FROM users WHERE username='{args['username']}'"
#         )[0]['id']
#         user: User = User.get(conn, id)
#
#         if user.login(args['username'], args['password']):
#             if login_user(user):
#                 return {"logged_in":True}
#             else:
#                 abort(401, "Login failed. Is your account active?")
#         else:
#             abort(401, "Login failed. Invalid credentials.")
# class LogoutUser(Resource):
#     @login_required
#     def post(self):
#         logout_user()
#
#
# api.add_resource(LoginUser, '/user/login')
# api.add_resource(LogoutUser, '/user/logout')
api.add_resource(RegisterUser, '/user/register')
api.add_resource(Card, '/card')
