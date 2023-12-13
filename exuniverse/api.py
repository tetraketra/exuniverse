import binascii
import os
import sqlite3
from collections import defaultdict
from datetime import datetime

from flask import Request, request
from flask_restful import Api, Resource, abort
from marshmallow import (Schema, ValidationError, fields, validates,
                         validates_schema)

from .app import flask_app
from .db import Card, User, flask_db
from .extras import abort_with_info, api_call_setup, get_hashed_password


class Post_UserRegister_InputSchema(Schema):
    username: str = fields.String(required=True) # Unique username of the new user.
    password: str = fields.String(required=True) # Plain password of the new user.
    email: str    = fields.String(required=True) # Unique email of the new user.


class UserRegister(Resource):
    def post(self):
        args = api_call_setup(request=request, schema=Post_UserRegister_InputSchema)
        salt: str = binascii.b2a_hex(os.urandom(5)).decode('utf-8')

        try:
            new_user = User(
                username      = args['username'],
                password      = get_hashed_password(args['password'], salt),
                password_salt = salt,
                email         = args['email']
            )

            flask_db.session.add(new_user)
            flask_db.session.commit()

            return { 'id':new_user.id } # SUCCESS

        except Exception as er:
            abort_with_info(args=args, er=er, source=self.post)


# class PostPut_Cards_InputSchema(Schema):
#     id                    = fields.Integer(required=False)
#     name                  = fields.String (required=False)
#     treated_as            = fields.String (required=False)
#     effect                = fields.String (required=False)
#     pic                   = fields.String (required=False)
#     template_type_id      = fields.Integer(required=False)
#     template_subtype_id   = fields.Integer(required=False)
#     template_attribute_id = fields.Integer(required=False)
#     monster_atk           = fields.Integer(required=False)
#     monster_def           = fields.Integer(required=False)
#     monster_is_gemini     = fields.Integer(required=False)
#     monster_is_spirit     = fields.Integer(required=False)
#     monster_is_toon       = fields.Integer(required=False)
#     monster_is_tuner      = fields.Integer(required=False)
#     monster_is_union      = fields.Integer(required=False)
#     monster_is_flip       = fields.Integer(required=False)
#     pendulum_scale        = fields.Integer(required=False)
#     pendulum_effect       = fields.String (required=False)
#     link_arrows           = fields.String (required=False)
#     ocg                   = fields.Integer(required=False)
#     ocg_date              = fields.Integer(required=False)
#     ocg_limit             = fields.Integer(required=False)
#     tcg                   = fields.Integer(required=False)
#     tcg_date              = fields.Integer(required=False)
#     tcg_limit             = fields.Integer(required=False)
#     exu_limit             = fields.Integer(required=False)
#     created_by_user_id    = fields.Integer(required=False)


class Get_Cards_InputSchema(Schema):
    id: list[int] = fields.List(fields.Integer, required=False) # List of card ids to get. If included, other filters will be ignored.
    name: list[str] = fields.List(fields.String, required=False) # List of card names to get.
    name_contains: list[str] = fields.List(fields.String, required=False) # List of strings to search card names for. Defaults to "or" searching unless `name_contains_all` is set to `True`.
    name_contains_all: bool = fields.Boolean(required=False, default=False) # Toggles card name search mode to "sequence" filtering (e.g. input ['foo', 'bar', 'bash'] will match "foo ... bar ... bash" but not "foo. bar bash", where "..." represents any run of characters that does not contain a period). Defaults to "disconnected" filtering. (e.g. input ['foo', 'bar'] will match "foo bar", "foo. bar", "foo", or "bar").
    name_contains_sequence: bool = fields.Boolean(required=False, default=False) # Toggles card name search mode to "sequence" filtering (e.g. input ['foo', 'bar', 'bash'] will match "foo ... bar ... bash" but not "foo. bar bash", where "..." represents any run of characters that does not contain a period). Defaults to "disconnected" filtering. (e.g. input ['foo', 'bar'] will match "foo bar", "foo. bar", "foo", or "bar").
    name_contains_not: bool = fields.Boolean(required=False, default=False) # Toggles card name searching to exclude any/all in `name_contains` (depending on `name_contains_all`).
    treated_as: list[str] = fields.List(fields.String, required=False) # List of card treated-as names to get.
    effect_contains: list[str] = fields.List(fields.String, required=False) # List of strings to search card effects for. Defaults to "or" searching unless `effect_contains_all` is set to `True`.
    effect_contains_all: bool = fields.Boolean(required=False, default=False) # Toggles card effect search mode to "all" filtering (e.g. input ['foo', 'bar'] will match "foo bar" but not "foo"). Defaults to "or" filtering (e.g. input ['foo', 'bar'] will match "foo bar", "foo", or "bar").
    effect_contains_sequence: bool = fields.Boolean(required=False, default=False) # Toggles card effect search mode to "sequence" filtering (e.g. input ['foo', 'bar', 'bash'] will match "foo ... bar ... bash" but not "foo. bar bash", where "..." represents any run of characters that does not contain a period). Defaults to "disconnected" filtering. (e.g. input ['foo', 'bar'] will match "foo bar", "foo. bar", "foo", or "bar").
    effect_contains_not: bool = fields.Boolean(required=False, default=False) # Toggles card effect searching to exclude any/all in `effect_contains` (depending on `effect_contains_all`).
    ttype: list[str] = fields.List(fields.String, required=False) # List of template types to get (e.g. ['monster', 'spell']).
    tsubtype: list[str] = fields.List(fields.String, required=False) # List of template subtypes to get (e.g. ['fusion', 'continuous']).
    attribute_contains: list[str] = fields.List(fields.String, required=False) # List of attributes to get (e.g. ['dark', 'earth', 'water', 'wind']). Defaults to "or" searching unless `attribute_contains_all` is set to `True`.
    attribute_contains_all: bool = fields.Boolean(required=False, default=False) # Toggles card attributes search mode to "all" filtering (e.g. input ['dark', 'light'] will match "dark/light" but not "dark"). Defaults to "or" filtering (e.g. input ['dark', 'light'] will match "dark/light", "dark", or "light").
    attribute_contains_not: bool = fields.Boolean(required=False, default=False) # Toggles card attributes searching to exclude any/all in `attribute_contains` (depending on `attribute_contains_all`).
    mon_atk: list[int] = fields.List(fields.Integer, required=False) # List of monster attacks to get.
    mon_atk_max: int = fields.Integer(required=False) # Maximum monster attack to get. Inclusive.
    mon_atk_min: int = fields.Integer(required=False) # Minimum monster attack to get. Inclusive.
    mon_atk_include_variadic: bool = fields.Boolean(required=False) # Specifies monster defense searching to include/exclude variadic ("?") attack cards. 
    mon_def: list[int] = fields.List(fields.Integer, required=False) # List of monster defenses to get.
    mon_def_max: int = fields.Integer(required=False) # Maximum monster defense to get. Inclusive.
    mon_def_min: int = fields.Integer(required=False) # Minimum monster defense to get. Inclusive.
    mon_def_include_variadic: bool = fields.Boolean(required=False) # Specifies monster defense searching to include/exclude variadic ("?") defense cards. 
    mon_level: list[int] = fields.List(fields.Integer, required=False) # List of monster levels to get (e.g. [1, 2, 10]).
    mon_level_max: int = fields.Integer(required=False) # Maximum monster level to get. Inclusive.
    mon_level_min: int = fields.Integer(required=False) # Minimum monster level to get. Inclusive.
    mon_level_not: bool = fields.Boolean(required=False, default=False) # Toggles monster level searching to exclude all in `mon_level`.
    pen_scale: list[int] = fields.List(fields.Integer, required=False) # List of pendulum scales to get.
    pen_scale_max: int = fields.Integer(required=False) # Maximum pendulum scale to get. Inclusive.
    pen_scale_min: int = fields.Integer(required=False) # Minimum pendulum scale to get. Inclusive.
    pen_effect_contains: list[str] = fields.List(fields.String, required=False) # List of strings to search pendulum effects for. Defaults to "or" searching unless `pen_effect_contains_all` is set to `True`.
    pen_effect_contains_all: bool = fields.Boolean(required=False, default=False) # Toggles card pendulum effect search mode to "all" filtering (e.g. input ['foo', 'bar'] will match "foo bar" but not "foo"). Defaults to "or" filtering (e.g. input ['foo', 'bar'] will match "foo bar", "foo", or "bar").
    pen_effect_contains_sequence: bool = fields.Boolean(required=False, default=False) # Toggles card pendulum effect search mode to "sequence" filtering (e.g. input ['foo', 'bar'] will match "foo ... bar" but not "foo. bar.", where "..." represents any run of characters that does not contain a period). Defaults to "disconnected" filtering. (e.g. input ['foo', 'bar'] will match "foo bar", "foo. bar", "foo", or "bar").
    pen_effect_contains_not: bool = fields.Boolean(required=False, default=False) # Toggles card pendulum effect searching to exclude any/all in `pen_effect_contains` (depending on `pen_effect_contains_all`).
    link_arrow_indices: list[int] = fields.List(fields.Integer, required=False) # List of link arrow indices to get (e.g. [0, 4] for up-left and/or down-right). You should use this in combination with `mon_level` to be more specific.
    format: list[str] = fields.List(fields.String, required=False) # List of card formats the gotten card may be in. Defaults to "or" searching unless `format_contains_all` is set to `True`.
    format_exact: bool = fields.Boolean(required=False, default=False) # Toggles card format search mode to "exact" filtering (e.g. input ['ocg', 'exu'] will match cards *only in* OCG and EXU). Defaults to "or" filtering (e.g. input ['ocg', 'exu'] will match cards in either OCG or EXU).
    created_by_user_id: list[int] = fields.List(fields.Integer, required=False) # List of user ids to get cards created by.
    created_by_user_name: list[str] = fields.List(fields.String, required=False) # List of user names to get cards created by.


class Cards(Resource):
    def get(self):
        ...

    def post(self):
        ...

    def put(self):
        ...


# ==== # ==== # ==== # ==== # ==== # ==== #

flask_api = Api(flask_app)
flask_api.add_resource(UserRegister, '/user/register')
flask_api.add_resource(Cards, '/cards')