from demands import HTTPServiceClient
from httpcache import CachingHTTPAdapter
from requests import auth


class JoolaAuth(auth.AuthBase):
    def __init__(self, api_token=None, user_token=None, username=None, password=None):
        self.username = username
        self.password = password
        self.api_token = api_token
        self.user_token = user_token

        if self.username and self.password and not self.api_token:
            raise TypeError('An API token was not provided.')

        if not self.username and self.password and self.api_token:
            raise TypeError('The username was not provided.')

        if self.username and not self.password and self.api_token:
            raise TypeError('The password was not provided.')

    def __call__(self, r):
        r.headers['Authorization'] = 'token %s' % self.user_token

        return r


class JoolaBaseClient(HTTPServiceClient):
    def __init__(self, *args, **kwargs):
        self.mount('http://', CachingHTTPAdapter())
        self.mount('https://', CachingHTTPAdapter())

        super(JoolaBaseClient, self).__init__(*args, **kwargs)