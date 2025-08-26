import pytest
from app import create_app, db
from app.services import GrupoService  # Asegurate que esté en app/services/__init__.py
from app.models import grupo as grupo_model
from test.instancias import nuevogrupo

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_crear_grupo(app_context):
    grupo = nuevogrupo(nombre="Grupo A")
    db.session.add(grupo)
    db.session.commit()

    assert grupo.id is not None
    assert grupo.nombre == "Grupo A"

def test_buscar_por_id(app_context):
    grupo = nuevogrupo(nombre="Grupo A")
    db.session.add(grupo)
    db.session.commit()

    resultado = GrupoService.buscar_por_id(grupo.id)
    assert resultado is not None
    assert resultado.nombre == "Grupo A"

def test_buscar_todos(app_context):
    db.session.add(nuevogrupo(nombre="Grupo A"))
    db.session.add(nuevogrupo(nombre="Grupo B"))
    db.session.commit()

    resultado = GrupoService.buscar_todos()
    nombres = [g.nombre for g in resultado]
    assert len(resultado) == 2
    assert "Grupo A" in nombres
    assert "Grupo B" in nombres

def test_actualizar_grupo(app_context):
    grupo = nuevogrupo(nombre="Grupo A")
    db.session.add(grupo)
    db.session.commit()

    grupo.nombre = "Grupo B"
    actualizado = GrupoService.actualizar(grupo.id, grupo)

    assert actualizado is not None
    assert actualizado.nombre == "Grupo B"

def test_borrar_grupo(app_context):
    grupo = nuevogrupo(nombre="Grupo A")
    db.session.add(grupo)
    db.session.commit()

    borrado = GrupoService.borrar_por_id(grupo.id)
    assert borrado is True

    resultado = GrupoService.buscar_por_id(grupo.id)
    assert resultado is None
