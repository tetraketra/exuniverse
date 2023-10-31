import os
import binascii

import sqlite3
from collections import defaultdict
from flask import request, Request
from flask_restful import Resource, abort
from marshmallow import Schema
from urllib.parse import urlparse, ParseResult

from ..db import get_db, query_db
from ..user import User
from .validation_schemas import *


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
    request: Request, schema: Schema, default_arg_value = None
) -> tuple[dict, sqlite3.Connection]:
    """
    Run this at the beginning of each Flask-RESTful GET/PUT/POST method to
    fetch the JSON input arguments and db connection object `conn`.
    """

    conn: sqlite3.Connection = get_db()
    args = defaultdict(lambda: default_arg_value, request.get_json(force=True))
    if schema:
        if er := schema().validate(request.json):
            abort(400, message=f"Argument parsing failed: {er}")

    return args, conn


class UserRegister(Resource):
    def post(self):
        args, conn = api_call_setup(request=request, schema=PostUserRegister_InputSchema)
        salt: str = binascii.b2a_hex(os.urandom(5)).decode('utf-8')
        sql: str = f"""
            INSERT INTO users (
                username, email,
                password, password_salt
            )
            VALUES (
                ?, ?,
                ?, ?
            );"""
        vals = (
            args['username'], args['email'],
            User.get_hashed_password(args['password'], salt), salt
        )

        try:
            new_user_id = query_db(conn=conn, sql=sql, vals=vals, method="insert")
            return { 'id':str(new_user_id) } # SUCCESS

        except sqlite3.Error as er:
            if er.sqlite_errorname == "SQLITE_CONSTRAINT_UNIQUE":
                abort(409, message=f"A user with that username already exists.")

            abort(400, message=f"Unhandled SQLite3 error: {er.sqlite_errorname}")


class Card(Resource):
    def get(self):
        args, conn = api_call_setup(request=request, schema=GetCard_InputSchema)
        select: str = f"* FROM cards" if args['return_style'] == 'joined' else f"""
                c.id, c.name, c.treated_as, c.effect, c.pic,
                tt.template_type, ts.template_subtype, ta.template_attribute,
                c.monster_atk, c.monster_def, mt.monster_type,
                c.monster_is_gemini, c.monster_is_spirit, c.monster_is_toon,
                c.monster_is_tuner, c.monster_is_union, c.monster_is_flip,
                c.pendulum_scale, c.pendulum_effect, c.link_arrows,
                c.ocg, ocg_date, c.ocg_limit,
                c.tcg, tcg_date, c.tcg_limit,
                c.exu_limit,
                u.username, c.date_created, c.date_updated
            FROM 
                cards c
                JOIN template_types tt ON c.template_type_id = tt.id
                JOIN template_subtypes ts ON c.template_subtype_id = ts.id
                LEFT JOIN template_attributes ta ON c.template_attribute_id = ta.id
                LEFT JOIN monster_types mt ON c.monster_type_id = mt.id
                LEFT JOIN users u ON c.created_by_user_id = u.id"""
        where: str = f"c.id = {args['id']}" if args['id'] else f"c.name = \"{args['name']}\""
        sql: str = f"SELECT {select} WHERE {where};"

        try:
            card = query_db(conn=conn, sql=sql, method="select")[0]
            return { **card } # SUCCESS
        
        except TypeError as er:
            abort(404, message=f"No card found with {where}!")
            
        except sqlite3.Error as er:
            abort(400, message=f"Unhandled SQLite3 error: {er.sqlite_errorname}")


    def post(self):
        args, conn = api_call_setup(request=request, schema=PostPutCard_InputSchema)
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
                created_by_user_id
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
            );"""
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
            args['created_by_user_id']
        )

        try:
            new_row_id = query_db(conn=conn, sql=sql, vals=vals, method="insert")
            return { 'id': new_row_id} # SUCCESS

        except sqlite3.Error as er:
            if er.sqlite_errorname == "SQLITE_CONSTRAINT_UNIQUE":
                abort(409, message=f"A card with that name already exists.")

            abort(400, message=f"Unhandled SQLite3 error: {er.sqlite_errorname}")


    def put(self):
        args, conn = api_call_setup(request=request, schema=PostPutCard_InputSchema)
        sql: str = f"""
            UPDATE cards
            SET
                name = ?, treated_as = ?, effect = ?, pic = ?,
                template_type_id = ?, template_subtype_id = ?, template_attribute_id = ?,
                monster_atk = ?, monster_def = ?, monster_type_id = ?,
                monster_is_gemini = ?, monster_is_spirit = ?, monster_is_toon = ?,
                monster_is_tuner = ?, monster_is_union = ?, monster_is_flip = ?,
                pendulum_scale = ?, pendulum_effect = ?,
                link_arrows = ?,
                ocg = ?, ocg_date = ?, ocg_limit = ?,
                tcg = ?, tcg_date = ?, tcg_limit = ?,
                exu_limit = ?,
                created_by_user_id = ?
            WHERE
                id = ?
            LIMIT 1;"""
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
            args['created_by_user_id'],
            args['id']
        )

        try:
            rows_affected = query_db(conn=conn, sql=sql, vals=vals, method="update")
            if not rows_affected:
                abort(404, message=f"No card found with id={args['id']}!")
            return { "id":args['id'] } # SUCCESS

        except sqlite3.Error as er:
            abort(400, message=f"Unhandled SQLite3 error: {er.sqlite_errorname}")


class Cards(Resource):
    def get(self): # TODO FIXME: TESTING
        args, conn = api_call_setup(request=request, schema=GetCards_InputSchema)

        _pmad = GetCards_InputSchema.parse_monster_atkdef

        if not args['name_method']: args['name_method'] = "like"
        if not args['treated_as_method']: args['treated_as_method'] = "like"
        if not args['effect_method']: args['effect_method'] = "like"
        if not args['pendulum_effect_method']: args['pendulum_effect_method'] = "like"
        
        select: str = f"""
                c.id, c.name, c.treated_as, c.effect, c.pic,
                tt.template_type, ts.template_subtype, ta.template_attribute,
                c.monster_atk, c.monster_def, mt.monster_type,
                c.monster_is_gemini, c.monster_is_spirit, c.monster_is_toon,
                c.monster_is_tuner, c.monster_is_union, c.monster_is_flip,
                c.pendulum_scale, c.pendulum_effect, c.link_arrows,
                c.ocg, ocg_date, c.ocg_limit,
                c.tcg, tcg_date, c.tcg_limit,
                c.exu_limit,
                u.username, c.date_created, c.date_updated
            FROM 
                cards c
                JOIN template_types tt ON c.template_type_id = tt.id
                JOIN template_subtypes ts ON c.template_subtype_id = ts.id
                LEFT JOIN template_attributes ta ON c.template_attribute_id = ta.id
                LEFT JOIN monster_types mt ON c.monster_type_id = mt.id
                LEFT JOIN users u ON c.created_by_user_id = u.id"""
        where: str = [
            f"c.name like '%{args['name']}%'" * (bool(args['name']) and (args['name_method'] == "like")),
            f"c.name = '{args['name']}'"      * (bool(args['name']) and (args['name_method'] == "exact")),
            f"c.treated_as like '%{args['treated_as']}%'" * (bool(args['treated_as']) and (args['treated_as_method'] == "like")),
            f"c.treated_as = '{args['treated_as']}'"      * (bool(args['treated_as']) and (args['treated_as_method'] == "exact")),
            f"c.effect like '%{args['effect']}%'" * (bool(args['effect']) and (args['effect_method'] == "like")),
            f"c.effect = '{args['effect']}'"      * (bool(args['effect']) and (args['effect_method'] == "exact")),
            f"tt.template_type in {*(args['template_type'] or ''),}" * bool(args['template_type']),
            f"ts.template_subtype in {*(args['template_subtype'] or ''),}" * bool(args['template_subtype']),
            f"ta.template_attribute in {*(args['template_attribute'] or ''),}" * bool(args['template_attribute']),
            f"{_pmad('c.monster_atk', args['monster_atk'])}" * bool(args['monster_atk']),
            f"{_pmad('c.monster_def', args['monster_def'])}" * bool(args['monster_def']),
            f"mt.monster_type in {*(args['monster_type'] or ''),}" * bool(args['monster_type']),
            f"c.monster_is_gemini = {args['monster_is_gemeni']}" * bool(args['monster_is_gemeni']),
            f"c.monster_is_spirit = {args['monster_is_spirit']}" * bool(args['monster_is_spirit']),
            f"c.monster_is_toon = {args['monster_is_toon']}" * bool(args['monster_is_toon']),
            f"c.monster_is_tuner = {args['monster_is_tuner']}" * bool(args['monster_is_tuner']),
            f"c.monster_is_union = {args['monster_is_union']}" * bool(args['monster_is_union']),
            f"c.monster_is_flip = {args['monster_is_flip']}" * bool(args['monster_is_flip']),
            f"c.pendulum_scale = {args['pendulum_scale']}" * bool(args['pendulum_scale']),
            f"c.pendulum_effect like '%{args['pendulum_effect']}%'" * (bool(args['pendulum_effect']) and (args['pendulum_effect_method'] == "like")),
            f"c.pendulum_effect = '{args['pendulum_effect']}'"      * (bool(args['pendulum_effect']) and (args['pendulum_effect_method'] == "exact")),
            f"c.link_arrows = '{args['link_arrows']}'" * bool(args['link_arrows']),
            f"c.ocg = {args['ocg']}" * bool(args['ocg']),
            f"c.ocg_limit = {args['ocg_limit']}" * bool(args['ocg_limit']),
            f"c.tcg = {args['tcg']}" * bool(args['tcg']),
            f"c.tcg_limit = {args['tcg_limit']}" * bool(args['tcg_limit']),
            f"c.exu_limit = {args['exu_limit']}" * bool(args['exu_limit']),
            f"u.username = '{args['username']}'" * bool(args['username'])
        ]
        where = " AND ".join(filter(None, where))
        sql: str = f"SELECT {select} WHERE {where};"

        try:
            print(sql)
            cards = query_db(conn=conn, sql=sql, method="select")
            return cards # SUCCESS

        except sqlite3.Error as er:
            abort(400, message=f"Unhandled SQLite3 error: {er.sqlite_errorname}")


class CardsNames(Resource):
    def get(self):
        _, conn = api_call_setup(request=request)
        sql: str = f"SELECT name FROM cards;"

        try:
            names = map(
                lambda row: row['name'], 
                query_db(conn=conn, sql=sql, method="update")
            )
            return { "names":[*names] }

        except sqlite3.Error as er:
            abort(400, message=f"Unhandled SQLite3 error: {er.sqlite_errorname}")


# # TODO: ACTUAL WEBPAGE STUFF INSTEAD OF API. DO NOT USE AUTH FOR API REQUESTS!
# # FIXME: Adjust to match https://flask-login.readthedocs.io/en/latest/#configuring-your-application
# #        once login form is ready.
# class UserLogin_InputSchema(Schema):
#     username = fields.String(required=True)
#     password = fields.String(required=True)
# class UserLogin(Resource):
#     def post(self):
#         args = request.get_json(force=True)
#         if er := UserLogin_InputSchema().validate(request.json):
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
# class UserLogout(Resource):
#     @login_required
#     def post(self):
#         logout_user()