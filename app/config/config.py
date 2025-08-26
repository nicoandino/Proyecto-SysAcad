import os
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).resolve().parents[2]
dotenv_path = basedir / '.env'
load_dotenv(dotenv_path)

# Logs de ayuda 
if os.getenv("FLASK_CONTEXT", "development") == "development":
    print(">>> Cargando config.py")
    print(">>> .env:", dotenv_path)
    print(">>> FLASK_CONTEXT:", os.getenv("FLASK_CONTEXT"))
    print(">>> DEV_DATABASE_URI:", os.getenv("DEV_DATABASE_URI"))

class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # DEFAULTS para Hashids (no romper si faltan en .env)
    HASHIDS_MIN_LENGTH = int(os.getenv('HASHIDS_MIN_LENGTH', '8'))
    HASHIDS_ALPHABET   = os.getenv('HASHIDS_ALPHABET', 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
    HASHIDS_SALT       = os.getenv('HASHIDS_SALT', 'change-me')

    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')


    @staticmethod
    def init_app(app):  # hook por si querés inicializaciones extras
        pass

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # Fallback seguro para evitar explotes en CI/local
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///:memory:')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True  # útil para ver SQL en consola
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI')

class ProductionConfig(Config):
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URI')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

def factory(app_context: str) -> type[Config]:
    """Devuelve la CLASE de config según el contexto."""
    configuration: dict[str, type[Config]] = {
        'testing': TestConfig,
        'development': DevelopmentConfig,
        'production': ProductionConfig
    }
    config_class = configuration.get(app_context)
    if config_class is None:
        raise ValueError(
            f"Contexto inválido: '{app_context}'. Debe ser 'testing', 'development' o 'production'."
        )
    return config_class
