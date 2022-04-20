
from unittest import TestCase
from django.test import Client
from peewee import *

from db.base import db

class BaseTestCase(TestCase):
    def __init__(self, models = [], methodName='runTest'):
        super().__init__(methodName)
        self.MODELS = models
        self.client = Client()
        self.test_db = db
    
    def setUp(self):
        with self.test_db:
            super(BaseTestCase, self).setUp()
            self.test_db.bind(self.MODELS, bind_refs=False, bind_backrefs=False)

            self.test_db.create_tables(self.MODELS)

    def tearDown(self):
        with self.test_db:
            super(BaseTestCase, self).tearDown()
            self.test_db.drop_tables(self.MODELS)
