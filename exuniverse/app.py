import os

from flask import Flask

from . import db
from . import os_addons


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping( # TODO: config files, actually secret secrets
    SECRET_KEY='CED0567CB8B29657FE1EB8132FAE5707FCD4C67DBF744CDDED5BDE7C0BD49594',
    DATABASE=os.path.join(app.instance_path, 'exuniverse.db'),
)

os_addons.ensure_dir(app.instance_path)

db.link_to_app(app)