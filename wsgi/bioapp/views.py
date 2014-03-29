from flask import render_template
from bioapp import bio

from mod_auth.forms import * #users can signin/signup from within our main page
from mod_auth.models import * #.. therefore we need the auth models

from mod_portfolio.forms import * #where the route is /<username>, users may CRUD their portfolio
from mod_portfolio.models import * #where the route is /<username> we must query users model

@bio.route('/')
@bio.route('/<username>')
def index(username=None):
    if username is None:
        return render_template('index.html', page_title='Biography just for you!', signin_form=SigninForm())

    user = Users.query.filter_by(username=username).first()
    if user is None:
        user = Users()
        user.username = username
        user.fullname = 'Batman, is that you?'
        user.tagline = 'Tagline of how special you are'
        user.bio = 'Explain to the rest of the world, why you are the very most unique person to look at'
        user.avatar = '/static/batman.jpeg'
        return render_template('themes/water/bio.html', page_title='Claim this name : ' + username, user=user,
                               signin_form=SigninForm(), portoform=PortoForm())
    else:
        return render_template('themes/water/bio.html', page_title=user.fullname, user=user, signin_form=SigninForm(),
                               portoform=PortoForm())