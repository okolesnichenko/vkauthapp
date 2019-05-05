from . import auth
from .. import db
from flask import redirect, url_for, flash
from .oauth import OAuthSignIn
from ..models import User
from flask_login import current_user, login_user, logout_user


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Функция вызова авторизации
@auth.route('/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

# Функция callback, для действия после авторизаци
@auth.route('/callback/<provider>')
def oauth_callback(provider):
    remember_me = True
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    oauth = OAuthSignIn.get_provider(provider)
    token, social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('main.index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, username=username, email=email, token=token)
        db.session.add(user)
        db.session.commit()
    else:
        if token != user.token:
            user.token = token
            db.session.commit()
    login_user(user, remember_me)
    return redirect(url_for('main.friends', social_id=social_id))
