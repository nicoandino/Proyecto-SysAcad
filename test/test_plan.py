import pytest
from datetime import date
from app import create_app, db
from app.services import PlanService  # Asegurate que esté en app/services/__init__.py
from test.instancias import nuevoplan, nuevaespecialidad

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

@pytest.fixture
def especialidad_base(app_context):
    especialidad = nuevaespecialidad(nombre="Neurología")
    db.session.add(especialidad)
    db.session.commit()
    return especialidad

def test_crear_plan(app_context, especialidad_base):
    plan = nuevoplan(
        nombre="Plan A",
        fecha_inicio=date(2024, 6, 1),
        fecha_fin=date(2024, 12, 1),
        observacion="Plan inicial",
        anio=2024,
        especialidad_id=especialidad_base.id
    )
    db.session.add(plan)
    db.session.commit()

    assert plan.id is not None
    assert plan.nombre == "Plan A"
    assert plan.fecha_inicio == date(2024, 6, 1)
    assert plan.fecha_fin == date(2024, 12, 1)
    assert plan.observacion == "Plan inicial"
    assert plan.anio == 2024
    assert plan.especialidad.nombre == "Neurología"

def test_buscar_por_id(app_context, especialidad_base):
    plan = nuevoplan(
        nombre="Plan A",
        fecha_inicio=date(2024, 6, 1),
        fecha_fin=date(2024, 12, 1),
        observacion="Plan inicial",
        anio=2024,
        especialidad_id=especialidad_base.id
    )
    db.session.add(plan)
    db.session.commit()

    resultado = PlanService.buscar_por_id(plan.id)
    assert resultado is not None
    assert resultado.nombre == "Plan A"
    assert resultado.fecha_inicio == date(2024, 6, 1)
    assert resultado.fecha_fin == date(2024, 12, 1)
    assert resultado.observacion == "Plan inicial"
    assert resultado.anio == 2024

def test_buscar_todos(app_context, especialidad_base):
    db.session.add(nuevoplan(
        nombre="Plan A",
        fecha_inicio=date(2024, 6, 1),
        fecha_fin=date(2024, 12, 1),
        observacion="Plan inicial",
        anio=2024,
        especialidad_id=especialidad_base.id
    ))
    db.session.add(nuevoplan(
        nombre="Plan B",
        fecha_inicio=date(2025, 1, 1),
        fecha_fin=date(2025, 6, 1),
        observacion="Segundo plan",
        anio=2025,
        especialidad_id=especialidad_base.id
    ))
    db.session.commit()

    planes = PlanService.buscar_todos()
    nombres = [p.nombre for p in planes]
    assert len(planes) >= 2
    assert "Plan A" in nombres
    assert "Plan B" in nombres

def test_actualizar_plan(app_context, especialidad_base):
    original = nuevoplan(
        nombre="Plan A",
        fecha_inicio=date(2024, 6, 1),
        fecha_fin=date(2024, 12, 1),
        observacion="Plan inicial",
        anio=2024,
        especialidad_id=especialidad_base.id
    )
    db.session.add(original)
    db.session.commit()

    original.nombre = "Plan Actualizado"
    original.fecha_inicio = date(2024, 7, 1)
    original.fecha_fin = date(2024, 12, 31)
    original.observacion = "Actualizado"
    actualizado = PlanService.actualizar(original.id, original)

    assert actualizado is not None
    assert actualizado.nombre == "Plan Actualizado"
    assert actualizado.observacion == "Actualizado"

def test_borrar_plan(app_context, especialidad_base):
    plan = nuevoplan(
        nombre="Plan A",
        fecha_inicio=date(2024, 6, 1),
        fecha_fin=date(2024, 12, 1),
        observacion="Plan inicial",
        anio=2024,
        especialidad_id=especialidad_base.id
    )
    db.session.add(plan)
    db.session.commit()

    borrado = PlanService.borrar_por_id(plan.id)
    assert borrado is True

    resultado = PlanService.buscar_por_id(plan.id)
    assert resultado is None
