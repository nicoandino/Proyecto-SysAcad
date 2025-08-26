import pytest
from app import create_app, db
from app.services import CategoriaCargoService  # Asegurate que esté en __init__.py
from app.models import categoriacargo as categoriacargo_model
from test.instancias import nuevacategoriacargo

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_crear_categoria(app_context):
    categoria = nuevacategoriacargo(nombre="Docente")
    db.session.add(categoria)
    db.session.commit()

    assert categoria is not None
    assert categoria.id is not None
    assert categoria.nombre == "Docente"

def test_buscar_por_id(app_context):
    categoria = nuevacategoriacargo(nombre="Docente")
    db.session.add(categoria)
    db.session.commit()

    resultado = CategoriaCargoService.buscar_por_id(categoria.id)
    assert resultado is not None
    assert resultado.nombre == "Docente"

def test_buscar_todos(app_context):
    db.session.add(nuevacategoriacargo(nombre="Docente"))
    db.session.add(nuevacategoriacargo(nombre="Investigador"))
    db.session.commit()

    categorias = CategoriaCargoService.buscar_todos()
    nombres = [c.nombre for c in categorias]
    assert len(categorias) == 2
    assert "Docente" in nombres
    assert "Investigador" in nombres

def test_actualizar_categoria(app_context):
    categoria = nuevacategoriacargo(nombre="Docente")
    db.session.add(categoria)
    db.session.commit()

    categoria.nombre = "Docente actualizado"
    actualizado = CategoriaCargoService.actualizar(categoria.id, categoria)
    assert actualizado is not None
    assert actualizado.nombre == "Docente actualizado"

def test_borrar_categoria(app_context):
    categoria = nuevacategoriacargo(nombre="Docente")
    db.session.add(categoria)
    db.session.commit()

    borrado = CategoriaCargoService.borrar_por_id(categoria.id)
    assert borrado is True
    resultado = CategoriaCargoService.buscar_por_id(categoria.id)
    assert resultado is None
