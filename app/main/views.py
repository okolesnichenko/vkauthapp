from flask import request, render_template, current_app
from flask_login import current_user
from . import main
from ..models import User
from .vkapi import VkApi


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/friends/<social_id>', methods=['GET', 'POST'])
def friends(social_id):
    user = User.query.filter_by(social_id=social_id).first()
    if user:
        api = VkApi(token=user.token)
        user = api.get_name(social_id)
        friends = api.get_friends()[0:5]
    return render_template('friends.html', friends=friends, user=user)
