import pytest
from xml.etree import ElementTree as ET
from app import create_app, db
from app.models import materia as materia_model
from test.instancias import nuevamateria

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_carga_datos_desde_xml(app_context):
    xml_data = """
    <materias>
        <materia>
            <nombre>Álgebra</nombre>
            <codigo>MAT101</codigo>
            <observacion>Obligatoria</observacion>
        </materia>
        <materia>
            <nombre>Análisis</nombre>
            <codigo>MAT102</codigo>
            <observacion>Optativa</observacion>
        </materia>
    </materias>
    """

    root = ET.fromstring(xml_data)
    for nodo in root.findall('materia'):
        nombre = nodo.find('nombre').text
        codigo = nodo.find('codigo').text
        observacion = nodo.find('observacion').text
        materia = nuevamateria(nombre=nombre, codigo=codigo, observacion=observacion)
        db.session.add(materia)

    db.session.commit()

    resultados = materia_model.Materia.query.all()
    assert len(resultados) == 2
    nombres = [m.nombre for m in resultados]
    assert "Álgebra" in nombres
    assert "Análisis" in nombres
