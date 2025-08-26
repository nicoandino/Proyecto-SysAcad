import pytest
from sqlalchemy import text
from app import create_app, db

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_db_connection(app_context):
    # Verificamos que la base responde a una consulta simple
    resultado = db.session.execute(text("SELECT 'Hello world'")).scalar()
    assert resultado == 'Hello world', "La base no respondió correctamente a la consulta."
