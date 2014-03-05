from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, HiddenField, TextAreaField, BooleanField
from wtforms.validators import Required, EqualTo, Optional, Length, Email

from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from flask import redirect, url_for, session
import os
import md5
import json
from collections import OrderedDict
from flask import jsonify
from sqlalchemy.ext import serializer

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') else 'postgresql://localhost:5432/bio'
application.config['CSRF_ENABLED'] = True
application.config['SECRET_KEY'] = 'rahasiabesar'

db = SQLAlchemy(application) 

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


class Users(db.Model, object):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    fullname = db.Column(db.String(101))
    password = db.Column(db.String)
    email = db.Column(db.String(100), unique=True)
    currently_live_in = db.Column(db.String(300))

    time_registered = db.Column(db.DateTime)
    tagline = db.Column(db.String(255))
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(255))

    active = db.Column(db.Boolean)
    
    portfolio = db.relationship('Portfolio')


    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active
    
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=True)
    description = db.Column(db.Text)
    tags = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result


class SignupForm(Form):
    email = TextField('Email address', validators=[
            Required('Please provide a valid email address'),
            Length(min=6, message=(u'Email address too short')),
            Email(message=(u'That\'s not a valid email address.'))
            ])
    password = PasswordField('Pick a secure password', validators=[
            Required(),
            Length(min=6, message=(u'Please give a longer password'))           
            ])
    username = TextField('Choose your username', validators=[Required()])
    agree = BooleanField('I agree all your <a href="/static/tos.html">Terms of Services</a>', validators=[Required(u'You must accept our Terms of Service')])

class SigninForm(Form):
    username = TextField('Username', validators=[
            Required(),
            validators.Length(min=3, message=(u'Your username must be a minimum of 3'))
            ])
    password = PasswordField('Password', validators=[
            Required(),
            validators.Length(min=6, message=(u'Please give a longer password'))
            ])
    remember_me = BooleanField('Remember me', default = False)


class PortoForm(Form):
    portfolio_id = HiddenField()
    title = TextField('Title', validators=[
            validators.Length(min=3, message=(u'Title must be longer, at least 3 characters'))
            ])
    description = TextField('Description', validators=[
            validators.Length(min=10, message=(u'Please give a longer description, at least 10 characters'))
            ])
    tags = TextField('Tags', validators=[
            validators.Length(min=2, message=(u'The tag at least having 2 characters length'))
            ])

@application.route('/')
@application.route('/<username>')
def index(username = None):
    if username is None:
        return render_template('index.html', page_title = 'Biography just for you!', signin_form = SigninForm())
    
    user = Users.query.filter_by(username=username).first()
    if user is None:
        user = Users()
        user.username = username
        user.fullname = 'Batman, is that you?'
        user.tagline = 'Tagline of how special you are'
        user.bio = 'Explain to the rest of the world, why you are the very most unique person to look at'
        user.avatar = '/static/batman.jpeg'
        return render_template('themes/water/bio.html', page_title = 'Claim this name : ' + username, user = user, signin_form = SigninForm(), portoform = PortoForm())
    else:
        return render_template('themes/water/bio.html', page_title = user.fullname, user = user, signin_form = SigninForm(), portoform = PortoForm())

@application.route('/signup', methods=['GET', 'POST'])
def signup():
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
                                       signin_form = SigninForm(),
                                       form = form,
                                       page_title = 'Signup to Bio Application')
            
            else:
                user.firstname = "Your fullname"
                user.password = hash_string(user.password)
                user.tagline = "Tagline of how special you are"
                user.bio = "Explain to the rest of the world why you are the very most unique person to have a look at"
                user.avatar = '/static/batman.jpeg'

                db.session.add(user)
                db.session.commit()
                return render_template('signup-success.html', 
                                       user = user,
                                       signin_form = SigninForm(),
                                       page_title = 'Sign Up Success!')

        else:
            return render_template('signup.html', 
                                   form = form, 
                                   signin_form = SigninForm(),
                                   page_title = 'Signup to Bio Application')
    return render_template('signup.html', 
                           form = SignupForm(), 
                           signin_form = SigninForm(),
                           page_title = 'Signup to Bio Application')

@application.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method=='POST':
        if current_user is not None and current_user.is_authenticated():
            return redirect(url_for('index'))
    
        form = SigninForm(request.form)
        if form.validate():
            user = Users.query.filter_by(username = form.username.data).first()
            if user is None:
                form.username.errors.append('Username not found')
                return render_template('signinpage.html',  signinpage_form = form, page_title = 'Sign In to Bio Application')
            if user.password != hash_string(form.password.data):
                form.password.errors.append('Passwod did not match')
                return render_template('signinpage.html',  signinpage_form = form, page_title = 'Sign In to Bio Application')

            login_user(user, remember = form.remember_me.data)            

            session['signed'] = True
            session['username']= user.username

            if session.get('next'):                
                next_page = session.get('next') 
                session.pop('next')
                return redirect(next_page) 
            else:
                return redirect(url_for('index'))
        return render_template('signinpage.html',  signinpage_form = form, page_title = 'Sign In to Bio Application')
    else:
        session['next'] = request.args.get('next')
        return render_template('signinpage.html', signinpage_form = SigninForm())        


@application.route('/signout')
@login_required
def signout():
    logout_user()
    session.pop('signed')
    session.pop('username')
    return redirect(url_for('index'))

@application.route('/profile')
@login_required
def profile():
    return render_template('profile.html', page_title='Customize your profile')

@application.route('/portfolio_add_update', methods = ['POST'])
@login_required #how to protect this in ajax called only for signed user?
def portfolio_add_update():

    form = PortoForm(request.form)
    if form.validate():
        result = {}
        result['iserror'] = False

        if not form.portfolio_id.data:
            user = Users.query.filter_by(username = session['username']).first()
            if user is not None:
                user.portfolio.append(Portfolio(title = form.title.data, description = form.description.data, tags = form.tags.data))
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

@application.route('/portfolio_get/<id>')
@login_required
def portfolio_get(id):
    portfolio = Portfolio.query.get(id)
    return json.dumps(portfolio._asdict())

@application.route('/portfolio_delete/<id>') 
@login_required
def portfolio_delete(id):
    portfolio = Portfolio.query.get(id)
    db.session.delete(portfolio)
    db.session.commit()
    result = {}
    result['result'] = 'success';
    return json.dumps(result)


def dbinit():
    db.create_all()
'''
    user = Users(username='ekowibowo', fullname='Eko Suprapto Wibowo', password=hash_string('rahasia'),
                         email='swdev.bali@gmail.com', 
                         tagline='A cool coder and an even cooler Capoeirista', 
                         bio = 'I love Python very much!', 
                         avatar = '/static/avatar.png',
                         active = True)
    user.portfolio.append(Portfolio(title = 'FikrPOS',
                                    description = 'An integrated POS solution using cloud concept', 
                                    tags='python,c#,openshift,flask,sqlalchemy,postgresql,bootstrap3'))
    user.portfolio.append(Portfolio(title = 'Bio Application',
                                    description = 'An autobiography publisher', 
                                    tags='python,openshift,flask,sqlalchemy,postgresql,bootstrap3'))
    user.portfolio.append(Portfolio(title = 'Project Management',
                                    description = 'Internal company project management tool', 
                                    tags='extjs,python,openshift,flask,sqlalchemy,postgresql,bootstrap3'))
    db.session.add(user)
    db.session.commit()
'''
@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
if __name__ == '__main__':
    dbinit()
    application.run(debug=True, host="0.0.0.0", port=8888)
