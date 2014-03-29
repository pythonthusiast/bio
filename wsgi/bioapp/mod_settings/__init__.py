from flask import Blueprint

mod_settings = Blueprint('settings', __name__)
from views import *

