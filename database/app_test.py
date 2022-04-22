from flask_testing import TestCase
from router import *
from models import *


class MyTest(TestCase):
    def create_app(self):
        return app
