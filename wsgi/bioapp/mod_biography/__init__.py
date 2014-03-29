from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from flask import Blueprint

mod_biography = Blueprint('biography', __name__)
from views import *

