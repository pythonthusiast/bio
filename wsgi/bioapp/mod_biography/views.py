import json
import os
from flask.ext.classy import FlaskView, route
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename

from bioapp.mod_biography import mod_biography
from flask import render_template, request
from bioapp.mod_auth import Users
from bioapp import db
from bioapp.config import Config
from bioapp import application


'''
This class still need security checking of id being given. It must be id of signed users
'''
class BiographyView(FlaskView):
    @route('edit_biography', methods=['POST'])
    @login_required
    def edit_biography(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        user.bio = request.form["value"]
        result = {}
        db.session.commit()
        return json.dumps(result)

    @route('edit_fullname', methods=['POST'])
    @login_required
    def edit_fullname(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        user.fullname = request.form["value"]
        result = {}
        db.session.commit()
        return json.dumps(result)  #or, as it is an empty json, you can simply use return "{}"

    @route('edit_tagline', methods=['POST'])
    @login_required
    def edit_tagline(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        user.tagline = request.form["value"]
        result = {}
        db.session.commit()
        return json.dumps(result)

    @route('upload_avatar', methods=['POST'])
    @login_required
    def upload_avatar(self):
        if request.method == 'POST':
            id = request.form["avatar_user_id"]
            file = request.files['file']
            if file and allowed_file(str.lower(str(file.filename))):
                user = Users.query.get(id)
                filename = user.username + "_" + secure_filename(file.filename)
                file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
                img = "/static/upload/" + filename

                user.avatar = img
                db.session.commit()
                return img

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS



BiographyView.register(mod_biography)