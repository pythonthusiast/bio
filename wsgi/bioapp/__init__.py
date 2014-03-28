import os
from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

basepath = os.path.dirname(__file__)
filepath = os.path.join(basepath, "..", "static")
application = Flask(__name__, static_folder=filepath)
application.config.from_object(Config)
db = SQLAlchemy(application)

print filepath
bioapp = Blueprint('BioApp', __name__, template_folder='templates')
from views import *

application.register_blueprint(bioapp)
