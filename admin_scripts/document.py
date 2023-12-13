import re
import inspect
from typing import NewType

from flask_restful import Resource
from marshmallow import Schema

from exuniverse.app import *
from exuniverse.db import *
from exuniverse.extras import *
from exuniverse.api import *

with open("README.md", "w") as fh:
    fh.truncate()

EXUNIVERSE_URL = "https://exuniverse.net"

header = """
# EXUniverse
The open-source custom card card API and battling website for Extinction Unleashed.

# Table of Contents
0. [Table of Contents](#table-of-contents) (you are here!)
1. [API Specification](#api-specification)

# API Specification
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
            api_documentation += f" - `{si['annotated_var_name']}`, {si['comment'][0].lower() + si['comment'][1:]}\n"

header = header.format(specification=api_documentation)

with open("README.md", "w") as fh:
    fh.write(header)

print(header)

