from faker import Factory
from httpcache import CachingHTTPAdapter
import httpretty
import mock
from nose2.tools import such

from pyjoola.client import JoolaBaseClient, APITokenAuth, Credentials


with such.A("Joola client") as it:
    @it.should("have no authentication mechanism if no credentials and no api token were provided")
    def test_have_no_authentication_mechanism_if_no_credentials_and_no_api_token_were_provided(case):
        faker = Factory.create()
        url = faker.uri()
        sut = JoolaBaseClient(url)

        case.assertIsNone(sut.session.auth)

    @it.should("select the API token authentication mechanism if an api token was provided")
    def test_select_the_api_token_authentication_mechanism_if_an_api_token_was_provided(case):
        faker = Factory.create()
        url = faker.uri()
        api_token = faker.sha256()
        sut = JoolaBaseClient(url, api_token=api_token)

        case.assertIsInstance(sut.session.auth, APITokenAuth)

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

        actual = sut.session.auth
        case.assertEqual(actual, expected)

    @it.should("mount the caching adapters on http://")
    def test_mount_the_caching_adapters_on_http(case):
        faker = Factory.create()
        url = faker.uri()
        sut = JoolaBaseClient(url)

        case.assertIn('http://', sut.session.adapters)
        case.assertIsInstance(sut.session.adapters['http://'], CachingHTTPAdapter)

    @it.should("mount the caching adapters on https://")
    def test_mount_the_caching_adapters_on_https(case):
        faker = Factory.create()
        url = faker.uri()
        sut = JoolaBaseClient(url)

        case.assertIn('https://', sut.session.adapters)
        case.assertIsInstance(sut.session.adapters['https://'], CachingHTTPAdapter)

    @it.should("retrieve all objects")
    def test_retrieve_all_objects(case):
        httpretty.enable()
        faker = Factory.create()
        url = faker.url()
        expected = str(faker.pydict())
        httpretty.register_uri(httpretty.GET, url, body=expected, content_type="application/json")

        sut = JoolaBaseClient(url)

        actual = sut.list().content.decode('utf-8')

        case.assertEqual(actual, expected)
        httpretty.disable()
        httpretty.reset()

    @it.should("retrieve one object by it's identifier")
    def test_retrieve_one_object_by_its_identifier(case):
        httpretty.enable()
        faker = Factory.create()
        url = faker.url()
        identifier = faker.slug()
        expected = str(faker.pydict())
        httpretty.register_uri(httpretty.GET, '%s%s' % (url, identifier), body=expected,
                               content_type="application/json")

        sut = JoolaBaseClient(url)

        actual = sut.get(identifier).content.decode('utf-8')

        case.assertEqual(actual, expected)
        httpretty.disable()
        httpretty.reset()

    @it.should("create one object")
    def test_create_one_object(case):
        httpretty.enable()
        faker = Factory.create()
        url = faker.url()
        sut = JoolaBaseClient(url)

        data = faker.pydict()
        expected = str(data)
        httpretty.register_uri(httpretty.POST, url, body=expected, content_type="application/json")

        actual = sut.insert(**data).content.decode('utf-8')

        case.assertEqual(actual, expected)
        httpretty.disable()
        httpretty.reset()

    @it.should("update one object by it's identifier")
    def test_update_one_object_by_its_identifier(case):
        httpretty.enable()
        faker = Factory.create()
        url = faker.url()
        identifier = faker.slug()
        sut = JoolaBaseClient(url)

        data = faker.pydict()
        expected = str(data)
        httpretty.register_uri(httpretty.PATCH, '%s%s' % (url, identifier), body=expected,
                               content_type="application/json")

        actual = sut.patch(identifier, **data).content.decode('utf-8')

        case.assertEqual(actual, expected)
        httpretty.disable()
        httpretty.reset()

    @it.should("delete one object by it's identifier")
    def test_delete_one_object_by_its_identifier(case):
        httpretty.enable()
        faker = Factory.create()
        url = faker.url()
        identifier = faker.slug()
        sut = JoolaBaseClient(url)

        data = faker.pydict()
        expected = str(data)
        httpretty.register_uri(httpretty.PATCH, '%s%s' % (url, identifier), body=expected,
                               content_type="application/json")

        actual = sut.patch(identifier, **data).content.decode('utf-8')

        case.assertEqual(actual, expected)
        httpretty.disable()
        httpretty.reset()

    it.createTests(globals())
