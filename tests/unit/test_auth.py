from faker import Factory
import httpretty
from nose2.tools import such
from pyjoola.client import JoolaAuth

with such.A("Joola authentication backend") as it:
    @it.should("raise a type error when username and password are provided but no API token is provided")
    def test_raise_a_type_error_when_username_and_password_are_provided_but_no_API_token_is_provided(case):
        faker = Factory.create()
        username = faker.simple_profile()['username']
        
        with case.assertRaisesRegexp(TypeError, "An API token was not provided."):
            JoolaAuth(username=username, password=faker.password())

    @it.should("raise a type error when password and the API token are provided but no username is provided")
    def test_raise_a_type_error_when_password_and_the_api_token_are_provided_but_no_API_token_is_provided(case):
        faker = Factory.create()

        with case.assertRaisesRegexp(TypeError, "The username was not provided."):
            JoolaAuth(api_token=faker.sha256(), password=faker.password())

    @it.should("raise a type error when username and the API token are provided but no password is provided")
    def test_raise_a_type_error_when_username_and_the_api_token_are_provided_but_no_API_token_is_provided(case):
        faker = Factory.create()
        username = faker.simple_profile()['username']

        with case.assertRaisesRegexp(TypeError, "The password was not provided."):
            JoolaAuth(api_token=faker.sha256(), username=username)

    it.createTests(globals())
