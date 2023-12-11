from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


db = SQLAlchemy(app)


class User(db.Model):
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username        = db.Column(db.String(80), unique=True, nullable=False)
    password        = db.Column(db.String(80), nullable=False)
    password_salt   = db.Column(db.String(80), nullable=False)
    email           = db.Column(db.String(120), unique=True, nullable=True)
    is_active       = db.Column(db.Boolean, default=False)
    pf_name         = db.Column(db.String(80), nullable=True)
    pf_about        = db.Column(db.Text, nullable=True)
    pfp_link        = db.Column(db.Text, nullable=True)
    date_created    = db.Column(db.DateTime(timezone=True), server_default=func.now())


class TemplateType(db.Model):
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ttype           = db.Column(db.String(20), nullable=False) # eg "monster", "spell", "trap"
    ttype_subtypes  = db.relationship('TemplateSubtype', backref='templatetype', lazy='joined')


class TemplateSubtype(db.Model):
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ttype_id        = db.Column(db.Integer, db.ForeignKey('template_type.id'), nullable=False)
    tsubtype        = db.Column(db.String(20), nullable=False) # eg "normal", "effect", "pendulum"


class Card(db.Model):
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name            = db.Column(db.String(120), nullable=False)
    treated_as      = db.Column(db.String(120), nullable=True)
    effect          = db.Column(db.Text, nullable=True)
    pic_link        = db.Column(db.Text, nullable=True)

    ttype_id        = db.Column(db.Integer, db.ForeignKey('template_type.id'), nullable=False) # eg "spell"'s id
    tsubtype_id     = db.Column(db.Integer, db.ForeignKey('template_subtype.id'), nullable=False) #eg "normal"'s id

    attributes      = db.Column(db.String(6), nullable=True) # "000000" for nothing, order: dark earth fire light water wind

    mon_atk         = db.Column(db.Integer, nullable=True)
    mon_def         = db.Column(db.Integer, nullable=True)
    mon_level       = db.Column(db.Integer, nullable=True)
    mon_abilities   = db.Column(db.String(6), nullable=True) # "000000" for nothing, order: flip gemini spirit toon tunter union
    mon_types       = db.Column(db.String(24), nullable=True) # "000000000000000000000000" for nothing, order: aqua beast beast-warrior creator god cyberse dinosaur divine-beast dragon fairy fiend fish illusion insect machine plant psychic pyro reptile rock sea serpent spellcaster thunder warrior winged beast wyrm zombie

    pen_scale       = db.Column(db.Integer, nullable=True)
    pen_effect      = db.Column(db.Text, nullable=True)

    link_arrows     = db.Column(db.String(8), nullable=True) # "00000000", read in clockwise spiral from top-left

    ocg             = db.Column(db.Boolean, nullable=True, default=0)
    ocg_date        = db.Column(db.DateTime(timezone=False), nullable=True)
    ocg_limit       = db.Column(db.Integer, nullable=True)
    tcg             = db.Column(db.Boolean, nullable=True, default=0)
    tcg_date        = db.Column(db.DateTime(timezone=False), nullable=True)
    tcg_limit       = db.Column(db.Integer, nullable=True)
    exu_limit       = db.Column(db.Integer, nullable=True, default=3)
    
    created_by_uid  = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # null means not created by a person
    date_updated    = db.Column(db.DateTime(timezone=True), server_default=func.now())
    date_created    = db.Column(db.DateTime(timezone=True), server_default=func.now())
