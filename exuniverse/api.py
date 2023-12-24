import binascii
import os
from typing import cast


from flask import request
from flask_restful import Api, Resource, abort
from marshmallow import Schema, fields
from sqlalchemy import func, text

from .app import flask_app
from .db import Card, TemplateSubtype, TemplateType, User, flask_db
from .extras import (abort_with_info, api_call_setup, get_hashed_password,
                     parse_query_string)


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


class Get_Cards_InputSchema(Schema):
    id: list[int] = fields.List(fields.Integer, required=False) # List of card ids to get. If included, other filters will be ignored.
    name: list[str] = fields.List(fields.String, required=False) # List of card names to get. If included, other filters will be ignored.
    treated_as: list[str] = fields.List(fields.String, required=False) # List of card treated-as names to get. If included, other filters will be ignored.
    
    name_contains: str = fields.String(required=False) # Query string to search card names.
    treated_as_contains: str = fields.String(required=False) # Query string to search card treated-as names.
    effect_contains: str = fields.String(required=False) # Query string to search card effects. 
    pen_effect_contains: str = fields.String(required=False) # Query string to search card pendulum effect. 

    # attribute_contains: str = fields.String(required=False) # Query string. # TODO FIXME HOW DO?

    t_type: list[str] = fields.List(fields.String, required=False) # List of card template types to get (e.g. ['Monster', 'Spell']).
    t_type_id: list[int] = fields.List(fields.Integer, required=False) # List of card template type ids to get (e.g. [1, 2]).
    t_subtype: list[str] = fields.List(fields.String, required=False) # List of card template subtypes to get (e.g. ['Fusion', 'Continuous']).
    t_subtype_id: list[int] = fields.List(fields.Integer, required=False) # List of card template subtype ids to get (e.g. [7, 8]).

    mon_atk: list[int] = fields.List(fields.Integer, required=False) # List of monster attacks to get (e.g. [100, 200, 4000]).
    mon_atk_max: int = fields.Integer(required=False) # Maximum monster attack to get. Inclusive (e.g. 4000).
    mon_atk_min: int = fields.Integer(required=False) # Minimum monster attack to get. Inclusive (e.g. 100).
    mon_atk_variadic: bool = fields.Boolean(required=False, missing=False) # Whether to include/exclude variadic ("?") attack cards. Defaults to `False`.
    mon_def: list[int] = fields.List(fields.Integer, required=False) # List of monster defenses to get (e.g. [100, 200, 4000]).
    mon_def_max: int = fields.Integer(required=False) # Maximum monster defense to get. Inclusive (e.g. 4000).
    mon_def_min: int = fields.Integer(required=False) # Minimum monster defense to get. Inclusive (e.g. 100).
    mon_def_variadic: bool = fields.Boolean(required=False, missing=False) # Whether to include/exclude variadic ("?") defense cards. Defaults to `False`.
    mon_level: list[int] = fields.List(fields.Integer, required=False) # List of monster levels to get (e.g. [1, 2, 10]).
    mon_level_max: int = fields.Integer(required=False) # Maximum monster level to get. Inclusive (e.g. 7).
    mon_level_min: int = fields.Integer(required=False) # Minimum monster level to get. Inclusive (e.g. 2).
    mon_level_not: bool = fields.Boolean(required=False, missing=False) # Makes `mon_level` exclusive rather than inclusive. Defaults to `False`.

    pen_scale: list[int] = fields.List(fields.Integer, required=False) # List of pendulum scales to get.
    pen_scale_max: int = fields.Integer(required=False) # Maximum pendulum scale to get. Inclusive.
    pen_scale_min: int = fields.Integer(required=False) # Minimum pendulum scale to get. Inclusive.
    
    link_arrow_indices: list[int] = fields.List(fields.Integer, required=False) # List of link arrow indices to get (e.g. [0, 4] for up-left and/or down-right). You should use this in combination with `mon_level` to be more specific.

    format: list[str] = fields.List(fields.String, required=False) # List of card formats the gotten card may be in. Defaults to "or" searching unless `format_contains_all` is set to `True`.
    format_exact: bool = fields.Boolean(required=False, missing=False) # Toggles card format search mode to "exact" filtering (e.g. input ['ocg', 'exu'] will match cards *only in* OCG and EXU). Defaults to "or" filtering (e.g. input ['ocg', 'exu'] will match cards in either OCG or EXU).

    created_by_user_id: list[int] = fields.List(fields.Integer, required=False) # List of user ids to get cards created by (e.g. [1, 2, 3]).
    created_by_user_name: list[str] = fields.List(fields.String, required=False) # List of usernames to get cards created by (e.g. ['user1', 'user2', 'user3']).


class Cards(Resource):
    def get(self):
        args = api_call_setup(request=request, schema=Get_Cards_InputSchema)
        query = Card.query

        if args['t_type'] or args['t_subtype']:
            query = query.join(TemplateType).join(TemplateSubtype)
        if args['t_subtype'] and not args['t_type']:
            abort(400, message="t_subtype requires t_type")
        if args['t_type']:
            query = query.filter(TemplateType.t_type.in_(args['t_type']))
        if args['t_subtype']:
            query = query.filter(TemplateSubtype.t_subtype.in_(args['t_subtype']))
        if args['t_type_id']:
            query = query.filter(Card.t_type_id.in_(args['t_type_id']))
        if args['t_subtype_id']:
            query = query.filter(Card.t_subtype_id.in_(args['t_subtype_id']))

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
            query = query.filter(Card.treated_as.op('regexp')(parse_query_string(args['treated_as_contains'])))

        if args['mon_atk']:
            query = query.filter(Card.mon_atk.in_(args['mon_atk']))
        if args['mon_atk_max']:
            query = query.filter(Card.mon_atk <= args['mon_atk_max'])
        if args['mon_atk_min']:
            query = query.filter(Card.mon_atk >= args['mon_atk_min'])
        if not args['mon_atk_variadic']:
            query = query.filter(Card.mon_atk_variadic == 0)

        if args['mon_def']:
            query = query.filter(Card.mon_def.in_(args['mon_def']))
        if args['mon_def_max']:
            query = query.filter(Card.mon_def <= args['mon_def_max'])
        if args['mon_def_min']:
            query = query.filter(Card.mon_def >= args['mon_def_min'])
        if not args['mon_def_variadic']:
            query = query.filter(Card.mon_def_variadic == 0)

        if any([args['pen_scale'], args['pen_scale_max'], args['pen_scale_min']]):
            query = query.filter(Card.pen_scale == 1)
        if args['pen_scale']:
            query = query.filter(Card.pen_scale.in_(args['pen_scale']))
        if args['pen_scale_max']:
            query = query.filter(Card.pen_scale <= args['pen_scale_max'])
        if args['pen_scale_min']:
            query = query.filter(Card.pen_scale >= args['pen_scale_min'])

        # TODO: ATTRIBUTES, MONSTER TYPES, ABILITIES, LINK ARROWS, FORMAT, CREATED BY %, 

        return [c.as_nice_dict() for c in cast(list[Card], query.all())]

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