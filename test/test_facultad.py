import pytest
from app import create_app, db
from app.models import facultad as facultad_model
from app.services import FacultadService  # Asegurate que esté en app/services/__init__.py
from test.instancias import nuevafacultad, nuevaautoridad

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_crear_facultad(app_context):
    autoridad = nuevaautoridad()
    facultad = nuevafacultad(autoridades=[autoridad])
    db.session.add(facultad)
    db.session.commit()

    assert facultad.id is not None
    assert facultad.nombre == "Facultad de Ciencias"
    assert facultad.facultad == 0
    assert facultad.universidad is not None
    assert facultad.universidad.nombre == "Universidad Nacional"
    assert autoridad in facultad.autoridades

def test_buscar_por_id(app_context):
    autoridad = nuevaautoridad()
    facultad = nuevafacultad(autoridades=[autoridad])
    db.session.add(facultad)
    db.session.commit()

    resultado = FacultadService.buscar_por_id(facultad.id)
    assert resultado is not None
    assert resultado.nombre == "Facultad de Ciencias"
    assert resultado.autoridades[0].nombre == autoridad.nombre

def test_buscar_todos(app_context):
    db.session.add(nuevafacultad())
    db.session.add(nuevafacultad(nombre="Facultad de Matemática"))
    db.session.commit()

    resultado = FacultadService.buscar_todos()
    nombres = [f.nombre for f in resultado]
    assert len(resultado) == 2
    assert "Facultad de Ciencias" in nombres
    assert "Facultad de Matemática" in nombres

def test_actualizar_facultad(app_context):
    facultad = nuevafacultad()
    db.session.add(facultad)
    db.session.commit()

    facultad.nombre = "Facultad de Ciencias Actualizada"
    resultado = FacultadService.actualizar_facultad(facultad.id, facultad)
    assert resultado is not None
    assert resultado.nombre == "Facultad de Ciencias Actualizada"

def test_borrar_facultad(app_context):
    facultad = nuevafacultad()
    db.session.add(facultad)
    db.session.commit()

    borrado = FacultadService.borrar_por_id(facultad.id)
    assert borrado is True

    resultado = FacultadService.buscar_por_id(facultad.id)
    assert resultado is None

def test_asociar_y_desasociar_autoridad(app_context):
    facultad = nuevafacultad()
    db.session.add(facultad)
    db.session.commit()

    autoridad = nuevaautoridad()
    facultad.asociar_autoridad(autoridad)
    db.session.commit()

    resultado = FacultadService.buscar_por_id(facultad.id)
    assert autoridad in resultado.autoridades

    facultad.desasociar_autoridad(autoridad)
    db.session.commit()

    resultado = FacultadService.buscar_por_id(facultad.id)
    assert autoridad not in resultado.autoridades
