import pytest
from app import create_app, db
from app.services import MateriaService  # Asegurate que esté en app/services/__init__.py
from test.instancias import nuevamateria, nuevaautoridad

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_crear_materia(app_context):
    autoridad = nuevaautoridad(nombre="Autoridad 1")
    materia = nuevamateria(nombre="Matematica", autoridades=[autoridad])
    db.session.add(materia)
    db.session.commit()

    assert materia.id is not None
    assert materia.nombre == "Matematica"
    assert autoridad in materia.autoridades

def test_buscar_por_id(app_context):
    materia = nuevamateria(nombre="Física")
    db.session.add(materia)
    db.session.commit()

    resultado = MateriaService.buscar_por_id(materia.id)
    assert resultado is not None
    assert resultado.nombre == "Física"

def test_buscar_todos(app_context):
    db.session.add(nuevamateria(nombre="Matematica 1"))
    db.session.add(nuevamateria(nombre="Matematica 2"))
    db.session.commit()

    resultado = MateriaService.buscar_todos()
    nombres = [m.nombre for m in resultado]
    assert len(resultado) >= 2
    assert "Matematica 1" in nombres
    assert "Matematica 2" in nombres

def test_actualizar_materia(app_context):
    materia = nuevamateria(nombre="Química")
    db.session.add(materia)
    db.session.commit()

    materia.nombre = "Química Orgánica"
    materia.codigo = "QO101"
    materia.observacion = "Nivel avanzado"
    actualizado = MateriaService.actualizar(materia.id, materia)

    assert actualizado is not None
    assert actualizado.nombre == "Química Orgánica"
    assert actualizado.codigo == "QO101"
    assert actualizado.observacion == "Nivel avanzado"

def test_borrar_materia(app_context):
    materia = nuevamateria(nombre="Biología")
    db.session.add(materia)
    db.session.commit()

    borrado = MateriaService.borrar_por_id(materia.id)
    assert borrado is True

    resultado = MateriaService.buscar_por_id(materia.id)
    assert resultado is None

def test_asociar_y_desasociar_autoridad(app_context):
    materia = nuevamateria(nombre="Historia")
    db.session.add(materia)
    db.session.commit()

    autoridad = nuevaautoridad(nombre="Autoridad 2")
    db.session.add(autoridad)
    db.session.commit()

    # Asociar
    MateriaService.asociar_autoridad(materia.id, autoridad.id)
    resultado = MateriaService.buscar_por_id(materia.id)
    assert autoridad in resultado.autoridades

    # Desasociar
    MateriaService.desasociar_autoridad(materia.id, autoridad.id)
    resultado = MateriaService.buscar_por_id(materia.id)
    assert autoridad not in resultado.autoridades
