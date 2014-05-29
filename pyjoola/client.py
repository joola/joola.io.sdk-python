from collections import namedtuple

from demands import HTTPServiceClient
from httpcache import CachingHTTPAdapter
from requests.auth import AuthBase


class APITokenAuth(AuthBase):
    def __init__(self, api_token):
        api_token = str(api_token)

        self.api_token = api_token

    def __call__(self, r):
        r.headers['Authorization'] = 'token %s' % self.api_token

        return r


class Credentials(namedtuple('CredentialsBase', ['workspace', 'username', 'password'])):
    def __new__(cls, workspace, username, password):
        workspace = str(workspace)
        username = str(username)
        password = str(password)

        return super(Credentials, cls).__new__(cls, workspace, username, password)


class JoolaBaseClient(HTTPServiceClient):
    def __init__(self, workspace=None, username=None, password=None, api_token=None, *args, **kwargs):
        self.mount('http://', CachingHTTPAdapter())
        self.mount('https://', CachingHTTPAdapter())

        if api_token:
            self.auth = APITokenAuth(api_token)
        elif workspace and username and password:
            self.auth = ('%s/%s' % (workspace, username), password)

        super(JoolaBaseClient, self).__init__(*args, **kwargs)