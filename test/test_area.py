import pytest
from app import create_app, db
from app.services import AreaService  # Asegurate que esté en app/services/__init__.py
from app.models import area as area_model
from test.instancias import nuevaarea

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_crear_area(app_context):
    area = nuevaarea()
    db.session.add(area)
    db.session.commit()

    assert area is not None
    assert area.id is not None
    assert area.nombre == "Matematica"

def test_buscar_por_id(app_context):
    area = nuevaarea()
    db.session.add(area)
    db.session.commit()

    resultado = AreaService.buscar_por_id(area.id)
    assert resultado is not None
    assert resultado.nombre == "Matematica"

def test_buscar_todos(app_context):
    db.session.add(nuevaarea(nombre="Matematica"))
    db.session.add(nuevaarea(nombre="Física"))
    db.session.commit()

    areas = AreaService.buscar_todos()
    nombres = [a.nombre for a in areas]
    assert len(areas) == 2
    assert "Matematica" in nombres
    assert "Física" in nombres

def test_actualizar_area(app_context):
    area = nuevaarea()
    db.session.add(area)
    db.session.commit()

    area.nombre = "Matemática Aplicada"
    actualizado = AreaService.actualizar(area.id, area)
    assert actualizado is not None
    assert actualizado.nombre == "Matemática Aplicada"

def test_borrar_area(app_context):
    area = nuevaarea()
    db.session.add(area)
    db.session.commit()

    borrado = AreaService.borrar_por_id(area.id)
    assert borrado is True
    resultado = AreaService.buscar_por_id(area.id)
    assert resultado is None
