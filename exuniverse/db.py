from .app import flask_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import event


flask_db = SQLAlchemy(flask_app)


class ModelRepr_BaseClass():
    def __repr__(self):
        d = {key:val for key, val in self.__dict__.items() if key[0] != '_'}
        return f"{self.__class__.__name__}{d}"

class User(flask_db.Model):
    id              = flask_db.Column(flask_db.Integer, primary_key=True, autoincrement=True)
    username        = flask_db.Column(flask_db.String(80), unique=True, nullable=False)
    password        = flask_db.Column(flask_db.String(80), nullable=False)
    password_salt   = flask_db.Column(flask_db.String(80), nullable=False)
    email           = flask_db.Column(flask_db.String(120), unique=True, nullable=True)
    is_active       = flask_db.Column(flask_db.Boolean, default=False)
    pf_name         = flask_db.Column(flask_db.String(80), nullable=True)
    pf_about        = flask_db.Column(flask_db.Text, nullable=True)
    pfp_link        = flask_db.Column(flask_db.Text, nullable=True)
    date_created    = flask_db.Column(flask_db.DateTime(timezone=True), server_default=func.now())


class TemplateType(ModelRepr_BaseClass, flask_db.Model):
    id              = flask_db.Column(flask_db.Integer, primary_key=True, autoincrement=True)
    ttype           = flask_db.Column(flask_db.String(20), nullable=False) # eg "monster", "spell", "trap"
    ttype_subtypes  = flask_db.relationship('TemplateSubtype', backref='templatetype', lazy='joined')


class TemplateSubtype(ModelRepr_BaseClass, flask_db.Model):
    id              = flask_db.Column(flask_db.Integer, primary_key=True, autoincrement=True)
    ttype_id        = flask_db.Column(flask_db.Integer, flask_db.ForeignKey('template_type.id'), nullable=False)
    tsubtype        = flask_db.Column(flask_db.String(20), nullable=False) # eg "normal", "effect", "pendulum"


class Card(flask_db.Model):
    id              = flask_db.Column(flask_db.Integer, primary_key=True, autoincrement=True)
    name            = flask_db.Column(flask_db.String(120), nullable=False, unique=True)
    treated_as      = flask_db.Column(flask_db.String(120), nullable=True)
    effect          = flask_db.Column(flask_db.Text, nullable=True)
    pic_link        = flask_db.Column(flask_db.Text, nullable=True)

    ttype_id        = flask_db.Column(flask_db.Integer, flask_db.ForeignKey('template_type.id'), nullable=False) # eg "spell"'s id
    tsubtype_id     = flask_db.Column(flask_db.Integer, flask_db.ForeignKey('template_subtype.id'), nullable=False) #eg "normal"'s id

    attributes      = flask_db.Column(flask_db.String(6), nullable=True) # "000000" for nothing, order: dark earth fire light water wind

    mon_atk         = flask_db.Column(flask_db.Integer, nullable=True)
    mon_def         = flask_db.Column(flask_db.Integer, nullable=True)
    mon_level       = flask_db.Column(flask_db.Integer, nullable=True)
    mon_abilities   = flask_db.Column(flask_db.String(6), nullable=True) # "000000" for nothing, order: flip gemini spirit toon tunter union
    mon_types       = flask_db.Column(flask_db.String(24), nullable=True) # "000000000000000000000000" for nothing, order: aqua beast beast-warrior creator god cyberse dinosaur divine-beast dragon fairy fiend fish illusion insect machine plant psychic pyro reptile rock sea serpent spellcaster thunder warrior winged beast wyrm zombie

    pen_scale       = flask_db.Column(flask_db.Integer, nullable=True)
    pen_effect      = flask_db.Column(flask_db.Text, nullable=True)

    link_arrows     = flask_db.Column(flask_db.String(8), nullable=True) # "00000000", read in clockwise spiral from top-left

    ocg             = flask_db.Column(flask_db.Boolean, nullable=True, default=0)
    ocg_date        = flask_db.Column(flask_db.DateTime(timezone=False), nullable=True)
    ocg_limit       = flask_db.Column(flask_db.Integer, nullable=True)
    tcg             = flask_db.Column(flask_db.Boolean, nullable=True, default=0)
    tcg_date        = flask_db.Column(flask_db.DateTime(timezone=False), nullable=True)
    tcg_limit       = flask_db.Column(flask_db.Integer, nullable=True)
    exu_limit       = flask_db.Column(flask_db.Integer, nullable=True, default=3)
    
    created_by_uid  = flask_db.Column(flask_db.Integer, flask_db.ForeignKey('user.id'), nullable=True) # null means not created by a person
    date_updated    = flask_db.Column(flask_db.DateTime(timezone=False), nullable=True)
    date_created    = flask_db.Column(flask_db.DateTime(timezone=False), server_default=func.now())
    date_deleted    = flask_db.Column(flask_db.DateTime(timezone=False), nullable=True)


@event.listens_for(Card, 'before_insert') 
def set_default_treated_as(mapper, connection, target): 
    if target.treated_as is None:
        target.treated_as = target.name
