import inspect
import re
from typing import NewType

from flask_restful import Resource
from marshmallow import Schema

from exuniverse.api import *
from exuniverse.app import *
from exuniverse.db import *
from exuniverse.extras import *

with open("README.md", "w") as fh:
    fh.truncate()

EXUNIVERSE_URL = "https://exuniverse.net"

header = """
# EXUniverse
The open-source custom card card API and battling website for Extinction Unleashed.

# Table of Contents
0. [Table of Contents](#table-of-contents) (you are here!)
1. [API Specification](#api-specification)
2. [Query Strings](#query-strings)

# API Specification
The following endpoints accept the following inputs in the request body as JSON:

{specification}
"""

with open("exuniverse/api.py", "r") as fh:
    endpoints = re.findall(r"add_resource\((\w*), [\'\"]([a-z\/]*)", fh.read())
    endpoints = dict(endpoints)

api_class_names = get_class_names_from_file("exuniverse/api.py")
api_classes = [globals()[cls] for cls in api_class_names]
api_documentation_sets = [{
    "endpoint":endpoints[cls.__name__],
    "get_schema":next(filter(lambda ac: "Get" in ac.__name__ and issubclass(ac, Schema) and f"_{cls.__name__}_" in ac.__name__, api_classes), None),
    "post_schema":next(filter(lambda ac: "Post" in ac.__name__ and issubclass(ac, Schema) and f"_{cls.__name__}_" in ac.__name__, api_classes), None),
    "put_schema":next(filter(lambda ac: "Put" in ac.__name__ and issubclass(ac, Schema) and f"_{cls.__name__}_" in ac.__name__, api_classes), None)
} for cls in api_classes if issubclass(cls, Resource)]

api_documentation = ""
for docset in api_documentation_sets:

    schemas = [docset['get_schema'], docset['post_schema'], docset['put_schema']]
    routes = ['GET', 'POST', 'PUT']

    _tmp = [both for both in zip(schemas, routes) if both[0] is not None]
    for schema, route in _tmp:

        api_documentation += f"`{route} {EXUNIVERSE_URL + docset['endpoint']}`\n"

        schema_inputs = get_schema_info(schema)
        for si in schema_inputs:
            api_documentation += f" - `{si['annotated_var_name']}`,{f" required" * si['required']} {si['comment'][0].lower() + si['comment'][1:]}\n"

        api_documentation += "\n"

header = header.format(specification=api_documentation)

header += """

# Query Strings
Query strings use square brackets `[]` to indicate text matching groups and
parentheses `()` to indicate logical condition groupings. For example,
`[FOO BAR]` `[FOO*BAR]` `[FOO**BAR]` `i[FOO**BAR]` `[FOO**BAR] & i[FOO*BAR]`
`[FOO*BAR] | !i[FOO**BAR]` `([FOO**BAR] & i[FOO*BAR]) | [BAR BASH]`
- `[` and `]` are used to indicate text matching groups.
- `(` and `)` are used to indicate logical condition groupings.
- `|` is used to indicate logical or.
- `&` is used to indicate logical and.
- `i` is used to indicate case-insensitive matching for the following match group.
- `!` is used to indicate negation for the following match group.
- `*` matches any number of characters between the left and right characters.
- `**` matches any number of characters between the left and right characters, excluding periods.

"""

with open("README.md", "w") as fh:
    fh.write(header)

print(header)

