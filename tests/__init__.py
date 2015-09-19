from flask_xxl.main import AppFactory
from .settings import BaseConfig

app = AppFactory(BaseConfig).get_app(__name__)


