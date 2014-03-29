from flask import Blueprint

mod_settings = Blueprint('settings', __name__, template_folder="templates")
from views import *

