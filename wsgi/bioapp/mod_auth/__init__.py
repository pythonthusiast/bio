from flask import Blueprint
from flask.ext.login import LoginManager

login_manager = LoginManager()
mod_auth = Blueprint('auth', __name__) #, url_prefix='/auth'
from views import *

@mod_auth.record_once
def on_load(state):
    login_manager.init_app(state.app)
    login_manager.login_view = '/auth/signin'

@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)