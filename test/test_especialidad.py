import pytest
from app import create_app, db
from app.services import EspecialidadService  # Asegurate que esté en app/services/__init__.py
from app.models import especialidad as especialidad_model
from test.instancias import nuevaespecialidad

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_crear_especialidad(app_context):
    especialidad = nuevaespecialidad()
    db.session.add(especialidad)
    db.session.commit()

    assert especialidad.id is not None
    assert especialidad.id >= 1
    assert especialidad.nombre == "Matematicas"
    assert especialidad.letra == "A"
    assert especialidad.tipoespecialidad.nombre == "Cardiologia"

def test_buscar_por_id(app_context):
    especialidad = nuevaespecialidad()
    db.session.add(especialidad)
    db.session.commit()

    resultado = EspecialidadService.buscar_por_id(especialidad.id)
    assert resultado is not None
    assert resultado.nombre == "Matematicas"
    assert resultado.letra == "A"

def test_buscar_todos(app_context):
    db.session.add(nuevaespecialidad())
    db.session.add(nuevaespecialidad())
    db.session.commit()

    resultado = EspecialidadService.buscar_todos()
    assert resultado is not None
    assert len(resultado) == 2

def test_actualizar_especialidad(app_context):
    especialidad = nuevaespecialidad()
    db.session.add(especialidad)
    db.session.commit()

    especialidad.nombre = "Matematica actualizada"
    resultado = EspecialidadService.actualizar(especialidad.id, especialidad)

    assert resultado is not None
    assert resultado.nombre == "Matematica actualizada"

def test_borrar_especialidad(app_context):
    especialidad = nuevaespecialidad()
    db.session.add(especialidad)
    db.session.commit()

    borrado = EspecialidadService.borrar_por_id(especialidad.id)
    assert borrado is True

    resultado = EspecialidadService.buscar_por_id(especialidad.id)
    assert resultado is None

def test_buscar_id_inexistente(app_context):
    resultado = EspecialidadService.buscar_por_id(9999)
    assert resultado is None

def test_letra_nula(app_context):
    especialidad = nuevaespecialidad(letra=None)
    db.session.add(especialidad)
    db.session.commit()

    resultado = EspecialidadService.buscar_por_id(especialidad.id)
    assert resultado.letra is None
