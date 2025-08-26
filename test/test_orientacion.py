import pytest
from datetime import date
from app import create_app, db
from app.services import OrientacionService  # Asegurate que esté en app/services/__init__.py
from test.instancias import nuevaorientacion, nuevaespecialidad, nuevoplan, nuevamateria

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

@pytest.fixture
def datos_relacionados(app_context):
    especialidad = nuevaespecialidad(nombre="Cardiología")
    plan = nuevoplan(nombre="Plan 2024", fecha_inicio=date(2024, 6, 4))
    materia = nuevamateria(nombre="Desarrollo", codigo="DEV101")
    db.session.add_all([especialidad, plan, materia])
    db.session.commit()
    return {"especialidad": especialidad, "plan": plan, "materia": materia}

def test_crear_orientacion(app_context, datos_relacionados):
    orientacion = nuevaorientacion(
        nombre="Orientación 1",
        especialidad_id=datos_relacionados["especialidad"].id,
        plan_id=datos_relacionados["plan"].id,
        materia_id=datos_relacionados["materia"].id
    )
    db.session.add(orientacion)
    db.session.commit()

    assert orientacion.id is not None
    assert orientacion.nombre == "Orientación 1"
    assert orientacion.especialidad.nombre == "Cardiología"
    assert orientacion.plan.fecha_inicio == date(2024, 6, 4)
    assert orientacion.materia.nombre == "Desarrollo"

def test_buscar_por_id(app_context, datos_relacionados):
    orientacion = nuevaorientacion(
        nombre="Orientación 1",
        especialidad_id=datos_relacionados["especialidad"].id,
        plan_id=datos_relacionados["plan"].id,
        materia_id=datos_relacionados["materia"].id
    )
    db.session.add(orientacion)
    db.session.commit()

    resultado = OrientacionService.buscar_por_id(orientacion.id)
    assert resultado is not None
    assert resultado.nombre == "Orientación 1"

def test_buscar_todos(app_context, datos_relacionados):
    db.session.add(nuevaorientacion(
        nombre="Orientación 1",
        especialidad_id=datos_relacionados["especialidad"].id,
        plan_id=datos_relacionados["plan"].id,
        materia_id=datos_relacionados["materia"].id
    ))
    db.session.add(nuevaorientacion(
        nombre="Orientación B",
        especialidad_id=datos_relacionados["especialidad"].id,
        plan_id=datos_relacionados["plan"].id,
        materia_id=datos_relacionados["materia"].id
    ))
    db.session.commit()

    orientaciones = OrientacionService.buscar_todos()
    nombres = [o.nombre for o in orientaciones]
    assert len(orientaciones) >= 2
    assert "Orientación 1" in nombres
    assert "Orientación B" in nombres

def test_actualizar_orientacion(app_context, datos_relacionados):
    original = nuevaorientacion(
        nombre="Orientación 1",
        especialidad_id=datos_relacionados["especialidad"].id,
        plan_id=datos_relacionados["plan"].id,
        materia_id=datos_relacionados["materia"].id
    )
    db.session.add(original)
    db.session.commit()

    original.nombre = "Orientación Actualizada"
    actualizada = OrientacionService.actualizar(original.id, original)

    assert actualizada is not None
    assert actualizada.nombre == "Orientación Actualizada"

def test_borrar_orientacion(app_context, datos_relacionados):
    orientacion = nuevaorientacion(
        nombre="Orientación 1",
        especialidad_id=datos_relacionados["especialidad"].id,
        plan_id=datos_relacionados["plan"].id,
        materia_id=datos_relacionados["materia"].id
    )
    db.session.add(orientacion)
    db.session.commit()

    borrado = OrientacionService.borrar_por_id(orientacion.id)
    assert borrado is True

    resultado = OrientacionService.buscar_por_id(orientacion.id)
    assert resultado is None
