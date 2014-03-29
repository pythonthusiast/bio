import os
from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

application = Flask(__name__, static_folder= os.path.join(os.path.dirname(__file__), "..", "static"))
application.config.from_object(Config)
db = SQLAlchemy(application)

bioapp = Blueprint('BioApp', __name__)
from views import *

from mod_auth import mod_auth
from mod_portfolio import mod_portfolio
from mod_biography import mod_biography
from mod_settings import mod_settings

application.register_blueprint(bioapp)
application.register_blueprint(mod_auth)
application.register_blueprint(mod_portfolio)
application.register_blueprint(mod_biography)
application.register_blueprint(mod_settings)
