import pytest
from app import create_app, db
from app.services import GradoService  # Asegurate que esté en app/services/__init__.py
from app.models import grado as grado_model
from test.instancias import nuevogrado

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_crear_grado(app_context):
    grado = nuevogrado(grado=1, nombre="Licenciatura en Informática", descripcion="Grado técnico")
    db.session.add(grado)
    db.session.commit()

    assert grado.id is not None
    assert grado.nombre == "Licenciatura en Informática"
    assert grado.descripcion == "Grado técnico"

def test_crear_grado_sin_descripcion(app_context):
    grado = nuevogrado(grado=2, nombre="Ingeniería en Sistemas", descripcion=None)
    db.session.add(grado)
    db.session.commit()

    assert grado.id is not None
    assert grado.descripcion == "Ingeniería en Sistemas"  # auto-completado por evento

def test_buscar_por_id(app_context):
    grado = nuevogrado(grado=3, nombre="Tecnicatura en Redes", descripcion="Redes y conectividad")
    db.session.add(grado)
    db.session.commit()

    resultado = GradoService.buscar_por_id(grado.id)
    assert resultado is not None
    assert resultado.nombre == "Tecnicatura en Redes"
    assert resultado.descripcion == "Redes y conectividad"

def test_buscar_todos(app_context):
    db.session.add(nuevogrado(grado=4, nombre="Bioinformática", descripcion="Interdisciplinario"))
    db.session.add(nuevogrado(grado=5, nombre="Matemática Aplicada", descripcion="Ciencias exactas"))
    db.session.commit()

    resultado = GradoService.buscar_todos()
    nombres = [g.nombre for g in resultado]
    assert len(resultado) == 2
    assert "Bioinformática" in nombres
    assert "Matemática Aplicada" in nombres

def test_actualizar_grado(app_context):
    grado = nuevogrado(grado=6, nombre="Física", descripcion="Ciencias naturales")
    db.session.add(grado)
    db.session.commit()

    grado.nombre = "Física Cuántica"
    grado.descripcion = "Estudios avanzados"
    actualizado = GradoService.actualizar(grado.id, grado)

    assert actualizado is not None
    assert actualizado.nombre == "Física Cuántica"
    assert actualizado.descripcion == "Estudios avanzados"

def test_borrar_grado(app_context):
    grado = nuevogrado(grado=7, nombre="Química", descripcion="Laboratorio")
    db.session.add(grado)
    db.session.commit()

    borrado = GradoService.borrar_por_id(grado.id)
    assert borrado is True

    resultado = GradoService.buscar_por_id(grado.id)
    assert resultado is None
