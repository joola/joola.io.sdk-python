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


class Credentials(namedtuple('CredentialsBase', ['username', 'password'])):
    def __new__(cls, workspace, username, password):
        workspace = str(workspace)
        username = '%s/%s' % (workspace, str(username))
        password = str(password)

        return super(Credentials, cls).__new__(cls, username, password)


class JoolaBaseClient(HTTPServiceClient):
    def __init__(self, url, credentials=None, api_token=None, **kwargs):
        super(JoolaBaseClient, self).__init__(url, **kwargs)

        self.mount('http://', CachingHTTPAdapter())
        self.mount('https://', CachingHTTPAdapter())

        if api_token:
            self.auth = APITokenAuth(api_token)
        elif credentials:
            self.auth = credentials

