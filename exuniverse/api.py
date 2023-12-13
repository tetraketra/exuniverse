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
    name: list[str] = fields.List(fields.String, required=False) # List of card names to get. If included, other filters will be ignored.
    treated_as: list[str] = fields.List(fields.String, required=False) # List of card treated-as names to get.
    effect_contains: list[str] = fields.List(fields.String, required=False) # List of strings to search card effects for. Defaults to "or" searching unless `effect_contains_all` is set to `True`.
    effect_contains_all: bool = fields.Boolean(required=False, default=False) # Toggles card effect search mode to "all" filtering (e.g. input ['foo', 'bar'] will match "foo bar" but not "foo"). Defaults to "or" (e.g. input ['foo', 'bar'] will match "foo bar", "foo", or "bar").
    ttype: list[str] = fields.List(fields.String, required=False) # List of template types to get (e.g. ['monster', 'spell']).
    tsubtype: list[str] = fields.List(fields.String, required=False) # List of template subtypes to get (e.g. ['fusion', 'continuous']).
    attribute_contains: list[str] = fields.List(fields.String, required=False) # List of attributes to get (e.g. ['dark', 'earth', 'water', 'wind']). Defaults to "or" searching unless `attribute_contains_all` is set to `True`.
    attribute_contains_all: bool = fields.Boolean(required=False, default=False) # Toggles card attributes search mode to "all" filtering (e.g. input ['dark', 'light'] will match "dark/light" but not "dark"). Defaults to "or" (e.g. input ['dark', 'light'] will match "dark/light", "dark", or "light").
    mon_atk: list[int] = fields.List(fields.Integer, required=False) # List of monster attacks to get.
    mon_atk_max: int = fields.Integer(required=False) # Maximum monster attack to get.
    mon_atk_min: int = fields.Integer(required=False) # Minimum monster attack to get.
    mon_def: list[int] = fields.List(fields.Integer, required=False) # List of monster defenses to get.
    mon_def_max: int = fields.Integer(required=False) # Maximum monster defense to get.
    mon_def_min: int = fields.Integer(required=False) # Minimum monster defense to get.
    mon_level: list[int] = fields.List(fields.Integer, required=False) # List of monster levels to get.
    mon_level_max: int = fields.Integer(required=False) # Maximum monster level to get.
    mon_level_min: int = fields.Integer(required=False) # Minimum monster level to get.
    pen_scale: list[int] = fields.List(fields.Integer, required=False) # List of pendulum scales to get.
    pen_effect_contains: list[str] = fields.List(fields.String, required=False) # List of strings to search pendulum effects for. Defaults to "or" searching unless `pen_effect_contains_all` is set to `True`.
    pen_effect_contains_all: bool = fields.Boolean(required=False, default=False) # Toggles card pendulum effect search mode to "all" filtering (e.g. input ['foo', 'bar'] will match "foo bar" but not "foo"). Defaults to "or" (e.g. input ['foo', 'bar'] will match "foo bar", "foo", or "bar").
    # LINK ARROWS CONTAINS ???
    # LINK ARROWS CONTAINS ALL ???
    ocg: bool = fields.Boolean(required=False) # Include only cards in or out of the ocg.
    tcg: bool = fields.Boolean(required=False) # Include only cards in or out of the tcg.
    created_by_user_id: list[int] = fields.List(fields.Integer, required=False) # List of user ids to get cards created by.
    created_by_user_name: list[str] = fields.List(fields.String, required=False) # List of user names to get cards created by.


class Cards(Resource):
    def get(self):
        ...

    def post(self):
        ...

    def put(self):
        # PUT NEEDS A SPECIAL ARGUMENT FOR CHANGING THE TREATED_AS FIELD AS WELL BY DEFAULT?
        ...


# ==== # ==== # ==== # ==== # ==== # ==== #

flask_api = Api(flask_app)
flask_api.add_resource(UserRegister, '/user/register')
flask_api.add_resource(Cards, '/cards')