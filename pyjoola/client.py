from collections import namedtuple

from httpcache import CachingHTTPAdapter
from requests import Session
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


class JoolaBaseClient(object):
    def __init__(self, base_url, credentials=None, api_token=None, **kwargs):
        self.base_url = str(base_url)
        self.session = Session()

        self.session.mount('http://', CachingHTTPAdapter())
        self.session.mount('https://', CachingHTTPAdapter())

        if api_token:
            self.session.auth = APITokenAuth(api_token)
        elif credentials:
            self.session.auth = credentials

    def list(self):
        return self.session.get(self.base_url)

    def get(self, lookup):
        return self.session.get('%s%s' % (self.base_url, str(lookup)))

    def insert(self, **kwargs):
        return self.session.post(self.base_url, data=kwargs)

    def patch(self, lookup, **kwargs):
        return self.session.patch('%s%s' % (self.base_url, str(lookup)), data=kwargs)

    def delete(self, lookup):
        return self.session.delete('%s%s' % (self.base_url, str(lookup)))

