from flask import render_template, request
from flask import redirect, url_for, session

from flask.ext.classy import FlaskView, route
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from forms import *
from models import *
from bioapp.mod_auth import mod_auth
from bioapp import application
import md5

def hash_string(string):
    salted_hash = string + application.config['SECRET_KEY']
    return md5.new(salted_hash).hexdigest()

class AuthView(FlaskView):
    @route('signin', methods=['GET', 'POST'])
    def signin(self):
        if request.method == 'POST':
            if current_user is not None and current_user.is_authenticated():
                return redirect(url_for('bio.index'))

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
                    return redirect(url_for('bio.index'))
            return render_template('signinpage.html', signinpage_form=form, page_title='Sign In to Bio Application')
        else:
            session['next'] = request.args.get('next')
            return render_template('signinpage.html', signinpage_form=SigninForm())


    #@route('/signout')
    @login_required
    def signout(self):
        session.clear()
        logout_user()
        return redirect(url_for('bio.index'))

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

AuthView.register(mod_auth)