import binascii
import os
import sqlite3
import json
import re
import more_itertools as mit
from collections import defaultdict
from datetime import datetime

from sqlalchemy import func, text
from flask import Request, request, jsonify
from flask_restful import Api, Resource, abort
from marshmallow import (Schema, ValidationError, fields, validates,
                         validates_schema)

from .app import flask_app
from .db import Card, User, flask_db
from .extras import abort_with_info, api_call_setup, get_hashed_password, parse_query_string


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
    treated_as: list[str] = fields.List(fields.String, required=False) # List of card treated-as names to get. If included, other filters will be ignored.
    
    name_contains: str = fields.String(required=False) # Query string.
    treated_as_contains: str = fields.String(required=False) # Query string.
    effect_contains: str = fields.String(required=False) # Query string. 
    # attribute_contains: str = fields.String(required=False) # Query string. # TODO COMPLICATED?

    ttype: list[str] = fields.List(fields.String, required=False) # List of template types to get (e.g. ['monster', 'spell']).
    tsubtype: list[str] = fields.List(fields.String, required=False) # List of template subtypes to get (e.g. ['fusion', 'continuous']).

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

    mon_level_not: bool = fields.Boolean(required=False, missing=False) # Toggles monster level searching to exclude all in `mon_level`.
    pen_scale: list[int] = fields.List(fields.Integer, required=False) # List of pendulum scales to get.
    pen_scale_max: int = fields.Integer(required=False) # Maximum pendulum scale to get. Inclusive.
    pen_scale_min: int = fields.Integer(required=False) # Minimum pendulum scale to get. Inclusive.

    pen_effect_contains: list[str] = fields.List(fields.String, required=False) # List of strings to search pendulum effects for. Defaults to "or" searching unless `pen_effect_contains_all` is set to `True`.
    pen_effect_contains_all: bool = fields.Boolean(required=False, missing=False) # Toggles card pendulum effect search mode to "all" filtering (e.g. input ['foo', 'bar'] will match "foo bar" but not "foo"). Defaults to "or" filtering (e.g. input ['foo', 'bar'] will match "foo bar", "foo", or "bar").
    pen_effect_contains_sequence: bool = fields.Boolean(required=False, missing=False) # Toggles card pendulum effect search mode to "sequence" filtering (e.g. input ['foo', 'bar'] will match "foo ... bar" but not "foo. bar.", where "..." represents any run of characters that does not contain a period). Defaults to "disconnected" filtering. (e.g. input ['foo', 'bar'] will match "foo bar", "foo. bar", "foo", or "bar").
    pen_effect_contains_ci: bool = fields.Boolean(required=False, missing=True) # Toggles card pendulum effect search mode to "case-insensitive" filtering (e.g. input ['foo', 'bar'] will match "FOO bar" but not "foo").
    not_pen_effect_contains: list[str] = fields.List(fields.String, required=False) # Same deal, but exclusion.
    not_pen_effect_contains_all: bool = fields.Boolean(required=False, missing=False) # Same deal, but exclusion.
    not_pen_effect_contains_sequence: bool = fields.Boolean(required=False, missing=False) # Same deal, but exclusion.
    not_pen_effect_contains_ci: bool = fields.Boolean(required=False, missing=True) # Same deal, but exclusion.
    
    link_arrow_indices: list[int] = fields.List(fields.Integer, required=False) # List of link arrow indices to get (e.g. [0, 4] for up-left and/or down-right). You should use this in combination with `mon_level` to be more specific.

    format: list[str] = fields.List(fields.String, required=False) # List of card formats the gotten card may be in. Defaults to "or" searching unless `format_contains_all` is set to `True`.
    format_exact: bool = fields.Boolean(required=False, missing=False) # Toggles card format search mode to "exact" filtering (e.g. input ['ocg', 'exu'] will match cards *only in* OCG and EXU). Defaults to "or" filtering (e.g. input ['ocg', 'exu'] will match cards in either OCG or EXU).

    created_by_user_id: list[int] = fields.List(fields.Integer, required=False) # List of user ids to get cards created by.
    created_by_user_name: list[str] = fields.List(fields.String, required=False) # List of user names to get cards created by.


class Cards(Resource):
    def get(self):
        args = api_call_setup(request=request, schema=Get_Cards_InputSchema)
        query = Card.query

        if args['id']:
            return [c.as_nice_dict() for c in Card.query.filter(Card.id.in_(args['id'])).all()]
        if args['name']:
            return [c.as_nice_dict() for c in Card.query.filter(Card.name.in_(args['name'])).all()]
        if args['treated_as']:
            return [c.as_nice_dict() for c in Card.query.filter(Card.treated_as.in_(args['treated_as'])).all()]

        if args['name_contains']:
            query = query.filter(Card.name.op('regexp')(parse_query_string(args['name_contains'])))
        if args['effect_contains']:
            query = query.filter(Card.effect.op('regexp')(parse_query_string(args['effect_contains'])))
        if args['treated_as_contains']:
            query = query.filter(Card.treated_as.op('treated_as')(parse_query_string(args['treated_as_contains'])))


        return [c.as_nice_dict() for c in query.all()]

    def post(self):
        # USER:PLAIN_PASS VALIDATION OR SESSION TOKEN VALIDATION 
        ...

    def put(self):
        # USER:PLAIN_PASS VALIDATION OR SESSION TOKEN VALIDATION
        ...


# ==== # ==== # ==== # ==== # ==== # ==== #

flask_api = Api(flask_app)
flask_api.add_resource(UserRegister, '/user/register')
flask_api.add_resource(Cards, '/cards')