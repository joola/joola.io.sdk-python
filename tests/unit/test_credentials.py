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

    it.createTests(globals())
