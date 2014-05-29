from demands import HTTPServiceClient
from httpcache import CachingHTTPAdapter
from requests.auth import AuthBase
import six


class APITokenAuth(AuthBase):
    def __init__(self, api_token):
        if not isinstance(api_token, six.string_types):
            raise TypeError('a string is required')

        self.api_token = api_token

    def __call__(self, r):
        r.headers['Authorization'] = 'token %s' % self.api_token

        return r


class JoolaBaseClient(HTTPServiceClient):
    def __init__(self, workspace=None, username=None, password=None, api_token=None, *args, **kwargs):
        self.mount('http://', CachingHTTPAdapter())
        self.mount('https://', CachingHTTPAdapter())

        if api_token:
            self.auth = APITokenAuth(api_token)
        else:
            self.auth = ('%s/%s' % (workspace, username), password)

        super(JoolaBaseClient, self).__init__(*args, **kwargs)