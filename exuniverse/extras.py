import ast
import inspect
import hashlib
from collections import defaultdict
from datetime import datetime
from importlib.util import module_from_spec, spec_from_file_location
from typing import Callable, Literal, Type, NewType

from flask import Request
from flask_restful import abort
from marshmallow import Schema


annotated_var_name = NewType('annotated_var_name', str)
comment = NewType('comment', str)
required = NewType('required', bool)
def get_schema_info(cls: Type) -> list[dict[annotated_var_name, comment, required]]:
    source_code = inspect.getsource(cls)

    output = []

    for line in source_code.split('\n'):
        line = line.strip()

        if 'fields.' in line:
            annotated_var_name, the_rest = line.split(' = ')
            output.append({
                "annotated_var_name":annotated_var_name.strip(), 
                "comment":the_rest.split(" # ")[1].strip(),
                "required":True if "True" in the_rest.split(" # ")[0] else False
            })

    return output


def get_class_names_from_file(file_path: str) -> list[str]:
    classes = []

    with open(file_path, "r") as file:
        tree = ast.parse(file.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)

    return classes


class DBConverter:
    attribute_order = ['dark', 'earth', 'fire', 'light', 'water', 'wind']
    ability_order = ['flip', 'gemini', 'spirit', 'toon', 'tuner', 'union']
    monster_type_order = ['aqua', 'beast', 'beast-warrior', 'creator god', 'cyberse', 'dinosaur', 'divine-beast', 'dragon', 'fairy', 'fiend', 'fish', 'illusion', 'insect', 'machine', 'plant', 'psychic', 'pyro', 'reptile', 'rock', 'sea serpent', 'spellcaster', 'thunder', 'warrior', 'winged beast', 'wyrm', 'zombie']


    @classmethod
    def get_order(cls, 
        converter: Literal['attribute', 'ability', 'monster_type']
    ) -> list[str]:
        
        match converter:
            case 'attribute':
                return cls.attribute_order
            case 'ability':
                return cls.ability_order
            case 'monster_type':
                return cls.monster_type_order


    @classmethod
    def str_to_list(cls, 
        converter: Literal['attribute', 'ability', 'monster_type'], 
        value: str
    ) -> list[str]:
        
        order = cls.get_order(converter)

        if len(order) != len(value):
            raise ValueError(f"Expected {len(order)} bits, got {len(value)}!")
        
        return [atr for atr, digit in zip(order, value) if digit == '1']


    @classmethod
    def list_to_str(cls, 
        converter: Literal['attribute', 'ability', 'monster_type'], 
        value: list[str]
    ) -> str:

        order = cls.get_order(converter)

        if len(order) != len(value):
            raise ValueError(f"Expected {len(order)} bits, got {len(value)}!")
        
        return ''.join([('1' if atr in value else '0') for atr in order])


def abort_with_info(
    args: defaultdict, er: Exception, source: Callable
) -> None:
    
    error_info = {
        "source":   source.__qualname__,
        "error":    (type(er), str(er)),
        "args":     args,
        "datetime": datetime.now(),
    }
    
    message = f"""
        Unhandled exception {error_info['error']} occurred in {error_info['source']}.
        Please contact an administrator and provide the following information:
        {error_info}
    """.replace("\n", " ").replace('\t', '')
                
    abort(400, message=message)


def get_hashed_password(
    password: str, password_salt: str
) -> str:
    
    return hashlib.sha256(
        (password + password_salt + "MHWVA7EFC79CVORN8G93VAZC6NT1BA").encode('utf-8')
    ).hexdigest()


def api_call_setup(
    request: Request, schema: Schema = None, default_arg_value = None
) -> defaultdict:
    """
    Run this at the beginning of each Flask-RESTful GET/PUT/POST 
    method to fetch the JSON input arguments.
    """
    
    args = defaultdict(lambda: default_arg_value, request.get_json(force=True))
    if schema:
        if er := schema().validate(request.json):
            abort(400, message=f"Argument parsing failed: {er}")

    return args