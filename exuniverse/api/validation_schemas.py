from marshmallow import Schema, fields, validates_schema, validates, ValidationError
from flask import request


class PostUserRegister_InputSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    email    = fields.String(required=True)
    

class GetCard_InputSchema(Schema):
    id           = fields.Integer(required=False)
    name         = fields.String (required=False)
    return_style = fields.String (required=False, default="joined")

    @validates_schema
    def validate_require_id_or_name(self, data, **kwargs):
        if not ('id' in data or 'name' in data):
            raise ValidationError('Must specify either field "id" or field "name"!')

    @validates('return_style')
    def validate_return_style(self, data, **kwargs):
        if not (data['return_style'] in ("joined", "unjoined")):
            raise ValidationError('Field "return_style" may only be "joined" or "unjoined"!') 


class PostPutCard_InputSchema(Schema):
    # REQUIRED: name, template_type_id, template_subtype_id, template_attribute_id
    id                    = fields.Integer(required=False)
    name                  = fields.String (required=True)
    treated_as            = fields.String (required=False)
    effect                = fields.String (required=False)
    pic                   = fields.String (required=False)
    template_type_id      = fields.Integer(required=True)
    template_subtype_id   = fields.Integer(required=True)
    template_attribute_id = fields.Integer(required=True)
    monster_atk           = fields.Integer(required=False)
    monster_def           = fields.Integer(required=False)
    monster_is_gemini     = fields.Integer(required=False)
    monster_is_spirit     = fields.Integer(required=False)
    monster_is_toon       = fields.Integer(required=False)
    monster_is_tuner      = fields.Integer(required=False)
    monster_is_union      = fields.Integer(required=False)
    monster_is_flip       = fields.Integer(required=False)
    pendulum_scale        = fields.Integer(required=False)
    pendulum_effect       = fields.String (required=False)
    link_arrows           = fields.String (required=False)
    ocg                   = fields.Integer(required=False)
    ocg_date              = fields.Integer(required=False)
    ocg_limit             = fields.Integer(required=False)
    tcg                   = fields.Integer(required=False)
    tcg_date              = fields.Integer(required=False)
    tcg_limit             = fields.Integer(required=False)
    exu_limit             = fields.Integer(required=False)
    created_by_user_id    = fields.Integer(required=False)

    @validates_schema
    def validate_id_for_post(self, data, **kwargs):
        if request.method == "PUT" and 'id' not in data:
            raise ValidationError('PUTs must populate field "id"! This allows PUTs to change field "name".') 


class GetCards_InputSchema(Schema):
    name                   = fields.String(required=False)
    name_method            = fields.String(required=False, default="like") # "exact" or "like"
    treated_as             = fields.String(required=False)
    treated_as_method      = fields.String(required=False, default="like") # "exact" or "like"
    effect                 = fields.String(required=False)
    effect_method          = fields.String(required=False, default="like") # "exact" or "like"
    template_type          = fields.List(cls_or_instance=fields.String,  required=False)
    template_subtype       = fields.List(cls_or_instance=fields.String,  required=False)
    template_attribute     = fields.List(cls_or_instance=fields.String,  required=False)
    monster_atk            = fields.String(required=False) # "1000" | "=1000" | ">1000" | "<=1000" | "500>x>1000" | "50<x<=100"
    monster_def            = fields.String(required=False) # "1000" | "=1000" | ">1000" | "<=1000" | "500>x>1000" | "50<x<=100"
    monster_type           = fields.List(cls_or_instance=fields.String,  required=False)
    monster_is_gemini      = fields.Integer(required=False)
    monster_is_spirit      = fields.Integer(required=False)
    monster_is_toon        = fields.Integer(required=False)
    monster_is_tuner       = fields.Integer(required=False)
    monster_is_union       = fields.Integer(required=False)
    monster_is_flip        = fields.Integer(required=False)
    pendulum_scale         = fields.Integer(required=False)
    pendulum_effect        = fields.String(required=False)
    pendulum_effect_method = fields.String(required=False, default="like") # "exact" or "like"
    link_arrows            = fields.String(required=False)
    ocg                    = fields.Integer(required=False)
    ocg_limit              = fields.Integer(required=False)
    tcg                    = fields.Integer(required=False)
    tcg_limit              = fields.Integer(required=False)
    exu_limit              = fields.Integer(required=False)
    created_by_user        = fields.String(required=False)

    @validates('name_method')
    def validate_name_method(self, value, **kwargs):
        if not ( value in ("exact", "like") ):
            raise ValidationError('Field "name_method" may only be "exact" or "like"!') 

    @validates('treated_as_method')
    def validate_name_method(self, value, **kwargs):
        if not ( value in ("exact", "like") ):
            raise ValidationError('Field "treated_as_method" may only be "exact" or "like"!') 

    @validates('effect_method')
    def validate_name_method(self, value, **kwargs):
        if not ( value in ("exact", "like") ):
            raise ValidationError('Field "effect_method" may only be "exact" or "like"!') 

    @validates('pendulum_effect_method')
    def validate_name_method(self, value, **kwargs):
        if not ( value in ("exact", "like") ):
            raise ValidationError('Field "pendulum_effect_method" may only be "exact" or "like"!') 

    @classmethod
    def parse_monster_atkdef(cls, field: str, val: str) -> str:          
        if not val:
            return ""
        
        val = val.replace(' ', '')  

        if val.isdigit():
            return f"{field} = {val}"

        if max(val.count('>'), val.count('<'), val.count('=')) == 1:
            return f"{field} {val}"

        if max(val.count('>'), val.count('<'), val.count('=')) > 1:
            #valinfo = [ *map(lambda c: CharInfo(c, c.isdigit(), c.isalpha()), val) ]

            first_val = "" # 100
            first_compare = "" # <=
            # something like "x" in between
            second_compare = "" # <
            second_val = "" # 1000
            
            left_half = True
            for c in val:
                if c.isdigit():
                    if left_half: first_val += c
                    else: second_val += c
                if c.isalpha():
                    left_half = False
                if not (c.isdigit() or c.isalpha()):
                    if left_half: first_compare += c
                    else: second_compare += c

            return f"{field} {first_compare} {first_val} AND {field} {second_compare} {second_val}"

        return ""