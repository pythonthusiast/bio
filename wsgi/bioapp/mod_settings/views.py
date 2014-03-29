from flask import render_template, request
from flask import redirect, url_for, session

from flask.ext.classy import FlaskView
from flask.ext.login import login_required
from bioapp.mod_settings import mod_settings

class SettingsView(FlaskView):
    @login_required
    def index(self):
        return render_template('profile.html', page_title='Customize your profile')

SettingsView.register(mod_settings)