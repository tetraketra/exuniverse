from flask_restful import Api

from ..app import app
from .validation_schemas import *
from .endpoints import *


app_api = Api(app)

# api.add_resource(UserLogin, '/user/login')
# api.add_resource(UserLogout, '/user/logout')
app_api.add_resource(UserRegister, '/user/register') # POST new user info to the users table. Takes unhashed password. 
app_api.add_resource(Card, '/card') # GET card by exact id or exact name. POST card with info. PUT card with info (requires id).
app_api.add_resource(Cards, '/cards') # GET cards by advanced querying.
app_api.add_resource(CardsNames, '/cards/names') # GET card _all_ card names.
