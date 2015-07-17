# -*- coding: utf-8 -*-
"""
    testing.py
    ~~~~~~~
    TestCase for testing
    :license: BSD3
"""
from flask.ext.testing import TestCase
from .main import AppFactory
from .basemodels import BaseMixin as BaseModel
from settings import TestingConfig
from sqlalchemy import MetaData

meta = BaseModel.metadata


class BaseTestCase(TestCase):

    def create_app(self):
        return AppFactory(TestingConfig).get_app(__name__)

    def setUp(self):
        self.app = self.create_app()
        self.db = BaseModel
        import sqlalchemy_utils as squ
        if squ.database_exists(self.db.engine.url):
            squ.drop_database(self.db.engine.url)
        squ.create_database(self.db.engine.url)
        #import imports
        #for module in dir(imports):
        #    globals()[module] = getattr(imports,module)            
        meta.bind = self.db.engine
        meta.create_all()

    def tearDown(self):
        self.db.session.close()
        meta.drop_all()


    def assertContains(self, response, text, count=None,
                       status_code=200, msg_prefix=''):
        """
        Asserts that a response indicates that some content was retrieved
        successfully, (i.e., the HTTP status code was as expected), and that
        ``text`` occurs ``count`` times in the content of the response.
        If ``count`` is None, the count doesn't matter - the assertion is true
        if the text occurs at least once in the response.
        """

        if msg_prefix:
            msg_prefix += ": "

        self.assertEqual(response.status_code, status_code,
            msg_prefix + "Couldn't retrieve content: Response code was %d"
                         " (expected %d)" % (response.status_code, status_code))

        real_count = response.data.count(text)
        if count is not None:
            self.assertEqual(real_count, count,
                msg_prefix + "Found %d instances of '%s' in response"
                             " (expected %d)" % (real_count, text, count))
        else:
            self.assertTrue(real_count != 0,
                    msg_prefix + "Couldn't find '%s' in response" % text)
