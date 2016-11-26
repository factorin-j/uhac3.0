from __future__ import unicode_literals
from urllib.parse import urlencode
from werkzeug.security import gen_salt
from requests import post
from base64 import b64encode
from uhac.settings import APP_CLIENT_ID
from uhac.settings import APP_CLIENT_SECRET
from uhac.settings import APP_CLIENT_REDIRECT_URL
from json import loads


OAUTH_SERVER_URL = 'https://bukas.org'


# noinspection PyMethodMayBeStatic
class Client(object):
    client_id = None
    client_secret = None
    redirect_url = None
    scopes = []
    access_token = None

    def __init__(self, data=None):
        self.client_id = APP_CLIENT_ID
        self.client_secret = APP_CLIENT_SECRET
        self.redirect_url = APP_CLIENT_REDIRECT_URL
        self.scopes = ['read', 'write']
        if data is not None:
            for k, v in data:
                setattr(self, k, v)

    def create_auth_url(self):
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

        response = post(token_url, data=data, headers=headers)
        json = loads(str(response.content), encoding='utf8')
        self.access_token = json.access_token

    def get_basic_auth_header(self):
        user_pass = '{0}:{1}'.format(self.client_id, self.client_secret)
        auth_string = b64encode(user_pass.encode('utf-8'))
        return 'Basic ' + auth_string.decode("utf-8")

    def api(self, uri, data=None):
        data = data or {}
        headers = {'authorization': 'Bearer ' + str(self.access_token)}
        response = post(OAUTH_SERVER_URL + uri, data=data, headers=headers)
        if response.content is None or type(response.content) != 'str':
            return None
        return loads(response.content)

client = Client()
