import pytest
from app import create_app, db
from app.models import departamento as departamento_model
from test.instancias import nuevodepartamento

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_nombre_vacio(app_context):
    departamento = nuevodepartamento(nombre="")
    db.session.add(departamento)
    with pytest.raises(Exception):
        db.session.commit()

def test_nombre_duplicado(app_context):
    db.session.add(nuevodepartamento(nombre="Química"))
    db.session.commit()

    duplicado = nuevodepartamento(nombre="Química")
    db.session.add(duplicado)
    with pytest.raises(Exception):
        db.session.commit()
