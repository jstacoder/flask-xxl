from flask_xxl.main import AppFactory
from test_settings import BaseConfig

def main():
    app = AppFactory(BaseConfig).get_app(__name__)

if __name__ == "__main__":
    main()
