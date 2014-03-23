import json
import md5
import os

from flask import render_template, request
from flask import redirect, url_for, session
from flask.ext.classy import FlaskView, route
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename

from main import application
from forms import *
from models import *
from config import Config


login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = '/signin'


@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)
def hash_string(string):
    """
    Return the md5 hash of a (string+salt)
    """
    salted_hash = string + application.config['SECRET_KEY']
    return md5.new(salted_hash).hexdigest()


@application.route('/')
@application.route('/<username>')
def index(username=None):
    print "1=", username
    if username is None:
        print "2=", username
        return render_template('index.html', page_title='Biography just for you!', signin_form=SigninForm())

    print "3=", username
    user = Users.query.filter_by(username=username).first()
    if user is None:
        print "4=", username
        user = Users()
        user.username = username
        user.fullname = 'Batman, is that you?'
        user.tagline = 'Tagline of how special you are'
        user.bio = 'Explain to the rest of the world, why you are the very most unique person to look at'
        user.avatar = '/static/batman.jpeg'
        return render_template('themes/water/bio.html', page_title='Claim this name : ' + username, user=user,
                               signin_form=SigninForm(), portoform=PortoForm())
    else:
        print "5=", username
        return render_template('themes/water/bio.html', page_title=user.fullname, user=user, signin_form=SigninForm(),
                               portoform=PortoForm())


class AuthView(FlaskView):
    @route('signin', methods=['GET', 'POST'])
    def signin(self):
        if request.method == 'POST':
            if current_user is not None and current_user.is_authenticated():
                return redirect(url_for('index'))

            form = SigninForm(request.form)
            if form.validate():
                user = Users.query.filter_by(username=form.username.data).first()
                if user is None:
                    form.username.errors.append('Username not found')
                    return render_template('signinpage.html', signinpage_form=form, page_title='Sign In to Bio Application')
                if user.password != hash_string(form.password.data):
                    form.password.errors.append('Passwod did not match')
                    return render_template('signinpage.html', signinpage_form=form, page_title='Sign In to Bio Application')

                login_user(user, remember=form.remember_me.data)

                session['signed'] = True
                session['username'] = user.username

                if session.get('next'):
                    next_page = session.get('next')
                    session.pop('next')
                    return redirect(next_page)
                else:
                    return redirect(url_for('index'))
            return render_template('signinpage.html', signinpage_form=form, page_title='Sign In to Bio Application')
        else:
            session['next'] = request.args.get('next')
            return render_template('signinpage.html', signinpage_form=SigninForm())


    #@route('/signout')
    @login_required
    def signout(self):
        session.clear()
        logout_user()
        return redirect(url_for('index'))

    @route('signup', methods=['GET', 'POST'])
    def signup(self):
        if request.method == 'POST':
            form = SignupForm(request.form)
            if form.validate():
                user = Users()
                form.populate_obj(user)

                user_exist = Users.query.filter_by(username=form.username.data).first()
                email_exist = Users.query.filter_by(email=form.email.data).first()

                if user_exist:
                    form.username.errors.append('Username already taken')

                if email_exist:
                    form.email.errors.append('Email already use')

                if user_exist or email_exist:
                    return render_template('signup.html',
                                           signin_form=SigninForm(),
                                           form=form,
                                           page_title='Signup to Bio Application')

                else:
                    user.firstname = "Your fullname"
                    user.password = hash_string(user.password)
                    user.tagline = "Tagline of how special you are"
                    user.bio = "Explain to the rest of the world why you are the very most unique person to have a look at"
                    user.avatar = '/static/batman.jpeg'
                    user.active = True

                    db.session.add(user)
                    db.session.commit()
                    return render_template('signup-success.html',
                                           user=user,
                                           signin_form=SigninForm(),
                                           page_title='Sign Up Success!')

            else:
                return render_template('signup.html',
                                       form=form,
                                       signin_form=SigninForm(),
                                       page_title='Signup to Bio Application')
        return render_template('signup.html',
                               form=SignupForm(),
                               signin_form=SigninForm(),
                               page_title='Signup to Bio Application')

class SettingsView(FlaskView):
    @login_required
    def index(self):
        return render_template('profile.html', page_title='Customize your profile')


class PortfolioView(FlaskView):
    @route('add_update', methods=['POST'])
    @login_required
    def add_update(self):
        form = PortoForm(request.form)
        if form.validate():
            result = {}
            result['iserror'] = False

            if not form.portfolio_id.data:
                user = Users.query.filter_by(username=session['username']).first()
                if user is not None:
                    user.portfolio.append(
                        Portfolio(title=form.title.data, description=form.description.data, tags=form.tags.data))
                    print 'id ', form.portfolio_id
                    db.session.commit()
                    result['savedsuccess'] = True
                else:
                    result['savedsuccess'] = False
            else:
                portfolio = Portfolio.query.get(form.portfolio_id.data)
                form.populate_obj(portfolio)
                db.session.commit()
                result['savedsuccess'] = True

            return json.dumps(result)

        form.errors['iserror'] = True
        print form.errors
        return json.dumps(form.errors)


    @route('get/<id>')
    @login_required
    def get(self, id):
        portfolio = Portfolio.query.get(id)
        return json.dumps(portfolio._asdict())


    @route('delete/<id>')
    @login_required
    def delete(self, id):
        portfolio = Portfolio.query.get(id)
        db.session.delete(portfolio)
        db.session.commit()
        result = {}
        result['result'] = 'success';
        return json.dumps(result)

class BiographyView(FlaskView):
    @route('edit_biography', methods=['POST'])
    def edit_biography(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        user.bio = request.form["value"]
        result = {}
        db.session.commit()
        return json.dumps(result)

    @route('edit_fullname', methods=['POST'])
    def edit_fullname(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        user.fullname = request.form["value"]
        result = {}
        db.session.commit()
        return json.dumps(result)  #or, as it is an empty json, you can simply use return "{}"

    @route('edit_tagline', methods=['POST'])
    def edit_tagline(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        user.tagline = request.form["value"]
        result = {}
        db.session.commit()
        return json.dumps(result)

    @route('upload_avatar', methods=['POST'])
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

AuthView.register(application)
PortfolioView.register(application)
BiographyView.register(application)
SettingsView.register(application)