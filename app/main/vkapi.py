import vk
import random
from flask import current_app

class VkApi():
    def __init__(self, token):
        self.session = vk.AuthSession(access_token=token, scope='wall, messages')
        self.vk_api = vk.API(self.session)
        self.current_version = current_app.config['VK_API_VERSION']

    def get_friends(self):
        users = []
        friends = self.vk_api.friends.get(v=self.current_version, fields='photo_50')
        if friends:
            friends_list = friends.get('items')
        else:
            return None
        return friends_list

    def get_name(self, social_id):
        username = self.vk_api.users.get(v=self.current_version, id=social_id)
        return username[0].get('first_name')