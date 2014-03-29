import json
from flask.ext.classy import FlaskView, route
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from bioapp.mod_portfolio import mod_portfolio
from models import *
from forms import *
from flask import render_template, request
from bioapp.mod_auth.models import Users
from flask import redirect, url_for, session

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

PortfolioView.register(mod_portfolio)