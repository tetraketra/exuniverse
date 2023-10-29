import os

from flask import Flask
from flask_restful import Resource, Api
from flask_login import LoginManager

from . import db
from . import os_addons

from .app import *
from .api import *
from .login_manager import *


if __name__ == "__main__":
    app.run(debug = True)
