from faker import Factory
from nose2.tools import such
from pretend import stub

from pyjoola.client import APITokenAuth


with such.A("Joola client") as it:

    it.createTests(globals())
