from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.sql import func

from .app import flask_app
from .extras import ModelRepr_BaseClass
from .reference import *

flask_db = SQLAlchemy(flask_app)


class User(ModelRepr_BaseClass, flask_db.Model, UserMixin):
    id              = flask_db.Column(flask_db.Integer, primary_key=True, autoincrement=True)
    username        = flask_db.Column(flask_db.String(80), unique=True, nullable=False)
    password        = flask_db.Column(flask_db.String(80), nullable=False)
    password_salt   = flask_db.Column(flask_db.String(64), nullable=False)
    email           = flask_db.Column(flask_db.String(80), unique=True, nullable=True)
    pf_name         = flask_db.Column(flask_db.String(80), nullable=True)
    pf_about        = flask_db.Column(flask_db.Text, nullable=True)
    pfp_link        = flask_db.Column(flask_db.Text, nullable=True)

    date_created    = flask_db.Column(flask_db.DateTime(timezone=True), server_default=func.now())


class TemplateType(ModelRepr_BaseClass, flask_db.Model):
    id              = flask_db.Column(flask_db.Integer, primary_key=True, autoincrement=True)
    ttype           = flask_db.Column(flask_db.String(20), nullable=False) # eg "monster", "spell", "trap"
    ttype_subtypes  = flask_db.relationship('TemplateSubtype', backref='template_type', lazy=True)


class TemplateSubtype(ModelRepr_BaseClass, flask_db.Model):
    id              = flask_db.Column(flask_db.Integer, primary_key=True, autoincrement=True)
    ttype_id        = flask_db.Column(flask_db.Integer, flask_db.ForeignKey('template_type.id'), nullable=False)
    tsubtype        = flask_db.Column(flask_db.String(20), nullable=False) # eg "normal", "effect", "pendulum"


class Card(ModelRepr_BaseClass, flask_db.Model):
    id              = flask_db.Column(flask_db.Integer, primary_key=True, autoincrement=True)
    name            = flask_db.Column(flask_db.String(MAX_CARD_NAME_LENGTH), nullable=False)
    treated_as      = flask_db.Column(flask_db.String(MAX_CARD_NAME_LENGTH), nullable=True)
    effect          = flask_db.Column(flask_db.Text, nullable=True)
    pic_link        = flask_db.Column(flask_db.Text, nullable=True)

    ttype_id        = flask_db.Column(flask_db.Integer, flask_db.ForeignKey('template_type.id'), nullable=False) # eg "spell"'s id
    tsubtype_id     = flask_db.Column(flask_db.Integer, flask_db.ForeignKey('template_subtype.id'), nullable=False) #eg "normal"'s id

    attributes      = flask_db.Column(flask_db.String(MAX_AT_AB_MT_LENGTH), nullable=True) # "000000" for nothing, order: dark earth fire light water wind

    mon_atk         = flask_db.Column(flask_db.Integer, nullable=True)
    mon_a_variadic  = flask_db.Column(flask_db.Boolean, nullable=True, default=0)
    mon_def         = flask_db.Column(flask_db.Integer, nullable=True)
    mon_d_variadic  = flask_db.Column(flask_db.Boolean, nullable=True, default=0)
    mon_level       = flask_db.Column(flask_db.Integer, nullable=True)
    mon_abilities   = flask_db.Column(flask_db.String(MAX_AT_AB_MT_LENGTH), nullable=True) # "000000" for nothing, order: flip gemini spirit toon tunter union
    mon_types       = flask_db.Column(flask_db.String(MAX_AT_AB_MT_LENGTH), nullable=True) # "000000000000000000000000" for nothing, order: aqua beast beast-warrior creator god cyberse dinosaur divine-beast dragon fairy fiend fish illusion insect machine plant psychic pyro reptile rock sea serpent spellcaster thunder warrior winged beast wyrm zombie

    pen             = flask_db.Column(flask_db.Boolean, nullable=True, default=0)
    pen_scale       = flask_db.Column(flask_db.Integer, nullable=True)
    pen_effect      = flask_db.Column(flask_db.Text, nullable=True)

    link_arrows     = flask_db.Column(flask_db.String(8), nullable=True) # "00000000", read in clockwise spiral from top-left

    serial_number   = flask_db.Column(flask_db.Integer, nullable=True)

    created_by_uid  = flask_db.Column(flask_db.Integer, flask_db.ForeignKey('user.id'), nullable=True) # null means not created by a person
    date_updated    = flask_db.Column(flask_db.DateTime(timezone=False), nullable=True)
    date_created    = flask_db.Column(flask_db.DateTime(timezone=False), server_default=func.now()) # utcnow
    date_deleted    = flask_db.Column(flask_db.DateTime(timezone=False), nullable=True)

    version_history = flask_db.relationship('CardVersionHistory', backref='card', lazy=True)
    cardpools       = flask_db.relationship('Cardpool', backref='card', lazy=True)


@event.listens_for(Card, 'before_insert')
def card_set_mon_a_d_variadic(mapper, connection, target):
    if target.mon_atk is None:
        target.mon_a_variadic = 1
    if target.mon_def is None:
        target.mon_d_variadic = 1
@event.listens_for(Card, 'after_update')
def card_update_date_updated(mapper, connection, target):
    connection.execute(
        Card.__table__.update()
        .where(Card.id == target.id)
        .values(date_updated=func.now())
    )
@event.listens_for(Card, 'before_update')
def card_port_to_version_history(mapper, connection, target):
    state = flask_db.inspect(target)
    original_values = {}

    for attr in state.attrs:
        hist = attr.load_history()

        if not hist.has_changes():
            original_values[attr.key] = getattr(target, attr.key)
            continue

        original_values[attr.key] = hist.deleted[0]

    connection.execute(
        CardVersionHistory.__table__.insert()
        .values(
            card_id=original_values['id'],
            name=original_values['name'],
            treated_as=original_values['treated_as'],
            effect=original_values['effect'],
            pic_link=original_values['pic_link'],
            ttype_id=original_values['ttype_id'],
            tsubtype_id=original_values['tsubtype_id'],
            attributes=original_values['attributes'],
            mon_atk=original_values['mon_atk'],
            mon_a_variadic=original_values['mon_a_variadic'],
            mon_def=original_values['mon_def'],
            mon_d_variadic=original_values['mon_d_variadic'],
            mon_level=original_values['mon_level'],
            mon_abilities=original_values['mon_abilities'],
            mon_types=original_values['mon_types'],
            pen=original_values['pen'],
            pen_scale=original_values['pen_scale'],
            pen_effect=original_values['pen_effect'],
            link_arrows=original_values['link_arrows'],
            serial_number=original_values['serial_number'],
            created_by_uid=original_values['created_by_uid'],
            date_introduced=(original_values['date_updated'] or original_values['date_created']),
        )
    )


class Format(ModelRepr_BaseClass, flask_db.Model):
    id              = flask_db.Column(flask_db.Integer, primary_key=True, autoincrement=True)
    name            = flask_db.Column(flask_db.String(20), nullable=False)
class Cardpool(ModelRepr_BaseClass, flask_db.Model):
    id              = flask_db.Column(flask_db.Integer, primary_key=True, autoincrement=True)
    card_id         = flask_db.Column(flask_db.Integer, flask_db.ForeignKey('card.id'), nullable=False)
    format_id       = flask_db.Column(flask_db.Integer, flask_db.ForeignKey('format.id'), nullable=False)

    limit           = flask_db.Column(flask_db.Integer, nullable=True, default=3) # limit 0 means banned
    date_integrated = flask_db.Column(flask_db.DateTime(timezone=False), nullable=True) # date added to format

    date_created    = flask_db.Column(flask_db.DateTime(timezone=False), server_default=func.now()) # utcnow
    date_updated    = flask_db.Column(flask_db.DateTime(timezone=False), nullable=True)

    
@event.listens_for(Cardpool, 'after_update')
def cardpool_update_date_updated(mapper, connection, target):
    connection.execute(
        Cardpool.__table__.update()
        .where(Cardpool.id == target.id)
        .values(date_updated=func.now())
    )


class CardVersionHistory(ModelRepr_BaseClass, flask_db.Model):
    row_id          = flask_db.Column(flask_db.Integer, primary_key=True, autoincrement=True)
    card_id         = flask_db.Column(flask_db.Integer, flask_db.ForeignKey('card.id'), nullable=False)
    date_introduced = flask_db.Column(flask_db.DateTime(timezone=False), nullable=False)
    date_obsoleted  = flask_db.Column(flask_db.DateTime(timezone=False), server_default=func.now()) # utcnow

    name            = flask_db.Column(flask_db.String(MAX_CARD_NAME_LENGTH), nullable=False)
    treated_as      = flask_db.Column(flask_db.String(MAX_CARD_NAME_LENGTH), nullable=True)
    effect          = flask_db.Column(flask_db.Text, nullable=True)
    pic_link        = flask_db.Column(flask_db.Text, nullable=True)

    ttype_id        = flask_db.Column(flask_db.Integer, flask_db.ForeignKey('template_type.id'), nullable=False) # eg "spell"'s id
    tsubtype_id     = flask_db.Column(flask_db.Integer, flask_db.ForeignKey('template_subtype.id'), nullable=False) #eg "normal"'s id

    attributes      = flask_db.Column(flask_db.String(MAX_AT_AB_MT_LENGTH), nullable=True) # "000000" for nothing, order: dark earth fire light water wind

    mon_atk         = flask_db.Column(flask_db.Integer, nullable=True)
    mon_a_variadic  = flask_db.Column(flask_db.Boolean, nullable=True, default=0)
    mon_def         = flask_db.Column(flask_db.Integer, nullable=True)
    mon_d_variadic  = flask_db.Column(flask_db.Boolean, nullable=True, default=0)
    mon_level       = flask_db.Column(flask_db.Integer, nullable=True)
    mon_abilities   = flask_db.Column(flask_db.String(MAX_AT_AB_MT_LENGTH), nullable=True) # "000000" for nothing, order: flip gemini spirit toon tunter union
    mon_types       = flask_db.Column(flask_db.String(MAX_AT_AB_MT_LENGTH), nullable=True) # "000000000000000000000000" for nothing, order: aqua beast beast-warrior creator god cyberse dinosaur divine-beast dragon fairy fiend fish illusion insect machine plant psychic pyro reptile rock sea serpent spellcaster thunder warrior winged beast wyrm zombie

    pen             = flask_db.Column(flask_db.Boolean, nullable=True, default=0)
    pen_scale       = flask_db.Column(flask_db.Integer, nullable=True)
    pen_effect      = flask_db.Column(flask_db.Text, nullable=True)

    link_arrows     = flask_db.Column(flask_db.String(8), nullable=True) # "00000000", read in clockwise spiral from top-left

    serial_number   = flask_db.Column(flask_db.Integer, nullable=True)

    created_by_uid  = flask_db.Column(flask_db.Integer, flask_db.ForeignKey('user.id'), nullable=True) # null means not created by a person