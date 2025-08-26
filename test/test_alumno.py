import pytest
from app import create_app, db
from app.services import AlumnoService  # Asegurate que esté en app/services/__init__.py
from app.models import alumno as alumno_model
from test.instancias import nuevoalumno

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_crear_alumno(app_context):
    alumno = nuevoalumno()
    db.session.add(alumno)
    db.session.commit()

    assert alumno is not None
    assert alumno.nombre == "Juan"
    assert alumno.apellido == "Pérez"
    assert alumno.tipo_documento == "DNI"
    assert alumno.nro_legajo == 1001

def test_buscar_por_id(app_context):
    alumno = nuevoalumno()
    db.session.add(alumno)
    db.session.commit()

    resultado = AlumnoService.buscar_por_id(alumno.id)
    assert resultado is not None
    assert resultado.nombre == "Juan"
    assert resultado.apellido == "Pérez"

def test_buscar_todos(app_context):
    db.session.add(nuevoalumno(nro_legajo=1001))
    db.session.add(nuevoalumno(nombre="Pedro", apellido="Gómez", nro_documento=87654321,
                               tipo_documento="Pasaporte", nro_legajo=1002))
    db.session.commit()

    alumnos = AlumnoService.buscar_todos()
    assert len(alumnos) == 2

def test_actualizar(app_context):
    alumno = nuevoalumno()
    db.session.add(alumno)
    db.session.commit()

    alumno.nombre = "Juan Actualizado"
    actualizado = AlumnoService.actualizar(alumno.id, alumno)
    assert actualizado is not None
    assert actualizado.nombre == "Juan Actualizado"

def test_borrar(app_context):
    alumno = nuevoalumno()
    db.session.add(alumno)
    db.session.commit()

    borrado = AlumnoService.borrar_por_id(alumno.id)
    assert borrado is True

    resultado = AlumnoService.buscar_por_id(alumno.id)
    assert resultado is None
