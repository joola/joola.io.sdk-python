from faker import Factory
from nose2.tools import such
from pretend import stub

from pyjoola.client import APITokenAuth


with such.A("API authentication backend") as it:
    @it.should("assign the provided api token to the api_token attribute")
    def test_should_assign_the_provided_api_token_to_the_api_token_attribute(case):
        faker = Factory.create()
        expected = faker.sha256()

        sut = APITokenAuth(expected)

        actual = sut.api_token
        case.assertEqual(actual, expected)

    @it.should("return the request after authenticating")
    def test_return_the_request_after_authenticating(case):
        faker = Factory.create()
        api_token = faker.sha256()
        expected = stub(headers={})

        sut = APITokenAuth(api_token)

        actual = sut(expected)

        case.assertEqual(actual, expected)

    @it.should('add the authorization header to the request')
    def test_add_the_authorization_header_to_the_request(case):
        faker = Factory.create()
        api_token = faker.sha256()
        expected = 'Authorization'

        sut = APITokenAuth(api_token)

        authenticated_request = sut(stub(headers={}))

        actual = authenticated_request.headers
        case.assertIn(expected, actual)

    @it.should("add a header to the request with the provided api token")
    def test_add_a_header_to_the_request_with_the_provided_api_token(case):
        faker = Factory.create()
        api_token = faker.sha256()
        expected = 'token %s' % api_token

        sut = APITokenAuth(api_token)

        actual = sut(stub(headers={})).headers['Authorization']
        case.assertEqual(actual, expected)

    it.createTests(globals())
