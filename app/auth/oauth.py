from flask import current_app, url_for, redirect, request
from rauth import OAuth2Service
import vk
import json


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_key = credentials['key']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('auth.oauth_callback', provider=self.provider_name, scope='friends', _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class VkSignIn(OAuthSignIn):
    def __init__(self):
        super(VkSignIn, self).__init__('vk')
        self.service = OAuth2Service(
            name='vk',
            client_id='6969972',
            client_secret='7DKvs0BaDpI14cVgRfiU',
            base_url='https://api.vk.com/method/',
            access_token_url='https://oauth.vk.com/access_token',
            authorize_url='https://oauth.vk.com/authorize'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(scope='email', response_type='code',
                                                       redirect_uri=self.get_callback_url()))

    def callback(self):
        def get_username_from_email(email):
            return email[0:email.index('@')]
        if 'code' not in request.args:
            return None, None, None
        data = {'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_callback_url()}
        resp = self.service.get_raw_access_token(method='POST', data=data)
        userdata = resp.json()
        if userdata:
            return userdata.get('access_token'), str(userdata.get('user_id')), \
                   get_username_from_email(userdata.get('email')), userdata.get('email')
        else:
            return None, None, None
