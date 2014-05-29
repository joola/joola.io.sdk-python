from faker import Factory
from httpcache import CachingHTTPAdapter
import mock
from nose2.tools import such
from requests.auth import HTTPBasicAuth

from pyjoola.client import JoolaBaseClient, APITokenAuth, Credentials


with such.A("Joola client") as it:
    @it.should("have no authentication mechanism if no credentials and no api token were provided")
    def test_have_no_authentication_mechanism_if_no_credentials_and_no_api_token_were_provided(case):
        faker = Factory.create()
        url = faker.uri()
        sut = JoolaBaseClient(url)

        case.assertIsNone(sut.auth)

    @it.should("select the API token authentication mechanism if an api token was provided")
    def test_select_the_api_token_authentication_mechanism_if_an_api_token_was_provided(case):
        faker = Factory.create()
        url = faker.uri()
        api_token = faker.sha256()
        sut = JoolaBaseClient(url, api_token=api_token)

        case.assertIsInstance(sut.auth, APITokenAuth)

    @it.should("initialize the API token authentication mechanism with the provided api token")
    def test_have_no_authentication_mechanism_if_no_credentials_and_no_api_token_was_specified(case):
        faker = Factory.create()
        url = faker.uri()
        api_token = faker.sha256()
        with mock.patch('pyjoola.client.APITokenAuth') as mocked_api_token_auth:
            JoolaBaseClient(url, api_token=api_token)

        mocked_api_token_auth.assert_called_once_with(api_token)

    @it.should("initialize the basic HTTP authentication mechanism with the provided credentials")
    def test_initialize_the_basic_http_authentication_mechanism_with_the_provided_credentials(case):
        faker = Factory.create()
        url = faker.uri()
        workspace = faker.pystr()
        username = faker.pystr()
        password = faker.sha256()
        expected = Credentials(workspace, username, password)
        sut = JoolaBaseClient(url, credentials=expected)

        actual = sut.auth
        case.assertEqual(actual, expected)

    @it.should("mount the caching adapters on http://")
    def test_mount_the_caching_adapters_on_http(case):
        faker = Factory.create()
        url = faker.uri()
        sut = JoolaBaseClient(url)

        case.assertIn('http://', sut.adapters)
        case.assertIsInstance(sut.adapters['http://'], CachingHTTPAdapter)
        
    @it.should("mount the caching adapters on https://")
    def test_mount_the_caching_adapters_on_https(case):
        faker = Factory.create()
        url = faker.uri()
        sut = JoolaBaseClient(url)

        case.assertIn('https://', sut.adapters)
        case.assertIsInstance(sut.adapters['https://'], CachingHTTPAdapter)

    it.createTests(globals())
