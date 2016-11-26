from __future__ import unicode_literals
from urllib.parse import urlencode
from werkzeug.security import gen_salt
from requests import post
from base64 import b64encode
from uhac.settings import APP_CLIENT_ID
from uhac.settings import APP_CLIENT_SECRET
from uhac.settings import APP_CLIENT_REDIRECT_URL


OAUTH_SERVER_URL = 'https://bukas.org'


# noinspection PyMethodMayBeStatic
class Client:
    client_id = None
    client_secret = None
    redirect_url = None
    scopes = []

    @staticmethod
    def get_client():
        client = Client()
        client.client_id = APP_CLIENT_ID
        client.client_secret = APP_CLIENT_SECRET
        client.redirect_url = APP_CLIENT_REDIRECT_URL
        client.scopes = ['read', 'write']
        return client

    def create_auth_url(self):
        print(self.client_id)
        return OAUTH_SERVER_URL + '/o/authorize/?' + urlencode({
            'response_type': 'code',
            'redirect_url': self.redirect_url,
            'client_id': self.client_id,
            'scope': str(' ').join(self.scopes),
            'state': gen_salt(25)
        })

    def authorize(self, code, stream_id):
        token_url = OAUTH_SERVER_URL + '/o/token/'
        headers = {
            'authorization': self.get_basic_auth_header(),
            'content-type': 'application/x-www-form-urlencoded'
        }

        data = {
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_url,
            'code': code,
            'user_stream_id': str(stream_id)
        }

        return post(token_url, data=data, headers=headers)

    def get_basic_auth_header(self):
        user_pass = '{0}:{1}'.format(self.client_id, self.client_secret)
        auth_string = b64encode(user_pass.encode('utf-8'))
        return 'Basic ' + auth_string.decode("utf-8")
