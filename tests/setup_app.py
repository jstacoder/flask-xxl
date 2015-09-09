from flask_xxl.main import AppFactory
from flask_xxl.basemodels import BaseMixin as BaseModel
from test_settings import BaseConfig
from flask_testing import TestCase


class TestApp(TestCase):

    def setUp(self):
        BaseModel.metadata.bind = BaseModel.engine
        BaseModel.metadata.bind.echo = True
        BaseModel.metadata.create_all()
        
    def create_app(self):
        from . import app
        self.app = app
        self.client = self.app.test_client()
        return self.app

    def test_one(self):
        self.assertTrue(True)

    def test_two(self):
        self.assertEquals(set(['admin','page','auth']),set(self.app.blueprints.keys()))

    def test_three(self):
        res = self.client.get('/')
        self.assertEquals('',res.data)

    def test_four(self):
        res = self.client.get()


if __name__ == "__main__":
    main()
