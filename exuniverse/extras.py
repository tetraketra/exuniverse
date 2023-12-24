import ast
import re
import hashlib
import inspect
import itertools as it
import more_itertools as mit
from collections import defaultdict, deque
from datetime import datetime
from typing import Callable, Literal, NewType, Type, Iterator, cast

from flask import Request
from flask_restful import abort
from marshmallow import Schema

import exuniverse.reference as ref


class ModelRepr_BaseClass():
    def __repr__(self):
        return str(self.as_dict(True))

    def as_dict(self,
        condensed = False
    ) -> dict:

        d = {key:val for key, val in self.__dict__.items() if key[0] != '_'}

        if condensed:
            for key, val in d.items():
                if isinstance(val, str) and len(val) > 100 and val[-5:] == '00000':
                    d[key] = d[key].strip('0')

        return d


annotated_var_name = NewType('annotated_var_name', str)
comment = NewType('comment', str)
required = NewType('required', bool)
def get_schema_info(
    cls: Type
) -> list[dict[annotated_var_name, comment, required]]:

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


def get_class_names_from_file(
    file_path: str
) -> list[str]:

    classes = []

    with open(file_path, "r") as file:
        tree = ast.parse(file.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)

    return classes


class DBConverter:

    @staticmethod
    def get_order(
        converter: Literal['attribute', 'ability', 'monster_type']
    ) -> list[str]:

        match converter:
            case 'attribute':
                return ref.ATTRIBUTES
            case 'ability':
                return ref.ABILITIES
            case 'monster_type':
                return ref.MONSTER_TYPES


    @staticmethod
    def binarystr_to_list(
        converter: Literal['attribute', 'ability', 'monster_type'],
        value: str
    ) -> list[str]:

        order = DBConverter.get_order(converter)

        if len(order) != len(value):
            raise ValueError(f"Expected {len(order)} bits, got {len(value)}!")

        return [atr for atr, digit in zip(order, value) if digit == '1']


    @staticmethod
    def list_to_binarystr(
        converter: Literal['attribute', 'ability', 'monster_type'],
        value: list[str]
    ) -> str:

        order = DBConverter.get_order(converter)

        if len(order) != len(value):
            raise ValueError(f"Expected {len(order)} bits, got {len(value)}!")

        return ''.join([('1' if atr in value else '0') for atr in order])


    @staticmethod
    def ttype_to_ttype_id(
        ttype: str
    ) -> int:

        return ref.TTYPES.index(ttype) + 1

    


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

    try:
        args = defaultdict(lambda: default_arg_value, schema().load(request.get_json(force=True)))
    except Exception as er:
        abort(400, message=f"Argument parsing failed: {er}")
    if schema:
        if er := schema().validate(request.json):
            abort(400, message=f"Argument parsing failed: {er}")

    return args


def consume(
    iterator: Iterator, 
    n: int
) -> None:
    """
    Advance the iterator n-steps ahead. If n is none, consume entirely.
    """
    
    deque(it.islice(iterator, n), maxlen=0)


def parse_query_string(
    query_string: str
) -> str:
    """
    Parses a query string (see documentation) into a regex pattern.

    Query strings use square brackets `[]` to indicate text matching groups and
    parentheses `()` to indicate logical condition groupings. For example:
    `[FOO BAR]` `[FOO*BAR]` `[FOO**BAR]` `i[FOO**BAR]` `[FOO**BAR] & i[FOO*BAR]`
    `[FOO*BAR] | !i[FOO**BAR]` `([FOO**BAR] & i[FOO*BAR]) | [BAR BASH]`
    - `[` and `]` indicate text matching groups.
    - `(` and `)` clarify logical condition groupings.
    - `|` indicates logical or.
    - `&` indicates logical and.
    - `i` indicates case-insensitive matching for the following match group.
    - `!` indicates negation for the following match group.
    - `*` matches any number of characters between the left and right characters.
    - `**` matches any number of characters between the left and right characters, excluding periods.
    """

    regex = ""

    for i, char in enumerate(query_string):
        
        if char == '[':
            regex += "(?i)" if 'i' in query_string[max(0, i - 2):i] else "(?-i)" # case sensitivity
            regex += "(?!.*" if '!' in query_string[max(0, i - 2):i] else "(?=.*" # negation

            mtch_len = query_string[i:].index(']')
            mtch = query_string[(i+1):(i + mtch_len)] # match group within brackets

            iterator = mit.peekable(mtch)
            for mtch_char in iterator:
                if mtch_char == '*':
                    if iterator.peek(' ') == '*':
                        regex += "[^\\.]*"
                        consume(iterator, 1)

                else:
                    regex += re.escape(mtch_char)

            regex += ")"

        if char in ('|', '(', ')'):
            regex += char

    return regex