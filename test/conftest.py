import pytest
from app import create_app, db

@pytest.fixture(scope="function")
def app():
    app = create_app()
    with app.app_context():
        yield app

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def limpiar_base(app):
    db.session.rollback()
    db.drop_all()
    db.create_all()
    yield
    db.session.remove()
