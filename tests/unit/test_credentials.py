from faker import Factory
from nose2.tools import such

from pyjoola.client import Credentials


with such.A("Credentials tuple") as it:
    @it.should("assign the workspace argument to the workspace attribute")
    def test_assign_the_workspace_argument_to_the_workspace_attribute(case):
        faker = Factory.create()
        workspace = faker.pystr()
        username = faker.pystr()
        password = faker.pystr()
        sut = Credentials(workspace, username, password)

        case.assertEqual(sut.workspace, workspace)

    @it.should("assign the username argument to the username attribute")
    def test_assign_the_username_argument_to_the_username_attribute(case):
        faker = Factory.create()
        workspace = faker.pystr()
        username = faker.pystr()
        password = faker.pystr()
        sut = Credentials(workspace, username, password)

        case.assertEqual(sut.username, username)

    @it.should("assign the password argument to the password attribute")
    def test_assign_the_password_argument_to_the_password_attribute(case):
        faker = Factory.create()
        workspace = faker.pystr()
        username = faker.pystr()
        password = faker.pystr()
        sut = Credentials(workspace, username, password)

        case.assertEqual(sut.password, password)

    it.createTests(globals())
