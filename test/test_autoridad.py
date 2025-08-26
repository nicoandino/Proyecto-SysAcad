import pytest
from app import create_app, db
from app.services import AutoridadService  # Asegurate que esté en app/services/__init__.py
from test.instancias import nuevaautoridad, nuevacargo, nuevamateria, nuevafacultad

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

@pytest.fixture
def cargo_base(app_context):
    cargo = nuevacargo(nombre="Director")
    db.session.add(cargo)
    db.session.commit()
    return cargo

def test_crear_autoridad(app_context, cargo_base):
    materia = nuevamateria()
    facultad = nuevafacultad()
    db.session.add_all([materia, facultad])
    db.session.commit()

    autoridad = nuevaautoridad(cargo_id=cargo_base.id, materias=[materia], facultades=[facultad])
    db.session.add(autoridad)
    db.session.commit()

    assert autoridad.id is not None
    assert autoridad.nombre == "Pelo"
    assert materia in autoridad.materias
    assert facultad in autoridad.facultades

def test_buscar_por_id(app_context, cargo_base):
    autoridad = nuevaautoridad(cargo_id=cargo_base.id)
    db.session.add(autoridad)
    db.session.commit()

    resultado = AutoridadService.buscar_por_id(autoridad.id)
    assert resultado is not None
    assert resultado.nombre == autoridad.nombre

def test_buscar_todos(app_context, cargo_base):
    db.session.add(nuevaautoridad(cargo_id=cargo_base.id, nombre="Pelo1"))
    db.session.add(nuevaautoridad(cargo_id=cargo_base.id, nombre="Pelo2"))
    db.session.commit()

    autoridades = AutoridadService.buscar_todos()
    assert len(autoridades) >= 2

def test_actualizar_autoridad(app_context, cargo_base):
    autoridad = nuevaautoridad(cargo_id=cargo_base.id)
    db.session.add(autoridad)
    db.session.commit()

    autoridad.nombre = "Nombre Actualizado"
    autoridad.telefono = "987654321"
    autoridad.email = "nuevo@example.com"
    actualizado = AutoridadService.actualizar(autoridad.id, autoridad)

    assert actualizado.nombre == "Nombre Actualizado"
    assert actualizado.telefono == "987654321"
    assert actualizado.email == "nuevo@example.com"

def test_borrar_autoridad(app_context, cargo_base):
    autoridad = nuevaautoridad(cargo_id=cargo_base.id)
    db.session.add(autoridad)
    db.session.commit()

    borrado = AutoridadService.borrar_por_id(autoridad.id)
    assert borrado is True
    resultado = AutoridadService.buscar_por_id(autoridad.id)
    assert resultado is None

def test_asociar_y_desasociar_materia(app_context, cargo_base):
    autoridad = nuevaautoridad(cargo_id=cargo_base.id)
    materia = nuevamateria()
    db.session.add_all([autoridad, materia])
    db.session.commit()

    AutoridadService.asociar_materia(autoridad.id, materia.id)
    actualizado = AutoridadService.buscar_por_id(autoridad.id)
    assert materia in actualizado.materias

    AutoridadService.desasociar_materia(autoridad.id, materia.id)
    actualizado = AutoridadService.buscar_por_id(autoridad.id)
    assert materia not in actualizado.materias

def test_asociar_y_desasociar_facultad(app_context, cargo_base):
    autoridad = nuevaautoridad(cargo_id=cargo_base.id)
    facultad = nuevafacultad()
    db.session.add_all([autoridad, facultad])
    db.session.commit()

    AutoridadService.asociar_facultad(autoridad.id, facultad.id)
    actualizado = AutoridadService.buscar_por_id(autoridad.id)
    assert facultad in actualizado.facultades

    AutoridadService.desasociar_facultad(autoridad.id, facultad.id)
    actualizado = AutoridadService.buscar_por_id(autoridad.id)
    assert facultad not in actualizado.facultades
