import pytest
from xml.etree import ElementTree as ET
from app import create_app, db
from app.models import especialidad as especialidad_model
from test.instancias import nuevaespecialidad
import os

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_carga_especialidades_desde_xml(app_context):
    xml_file_path = os.path.join(
        os.path.dirname(__file__), '..', 'archivados_xml', 'especialidades.xml'
    )

    assert os.path.exists(xml_file_path), f"El archivo {xml_file_path} no existe."

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    for item in root.findall('_expxml'):
        especialidad_element = item.find('especialidad')
        nombre_element = item.find('nombre')
        observacion_element = item.find('observacion')

        if especialidad_element is not None and nombre_element is not None:
            especialidad = int(especialidad_element.text)
            nombre = nombre_element.text
            observacion = observacion_element.text if observacion_element is not None else None

            obj = nuevaespecialidad(especialidad=especialidad, nombre=nombre, observacion=observacion)
            db.session.add(obj)
        else:
            print(f"Item omitido por datos faltantes. Especialidad: {especialidad_element}, Nombre: {nombre_element}")

    db.session.commit()

    resultados = especialidad_model.Especialidad.query.all()
    assert len(resultados) > 0, "No se insertaron datos en la base de datos."
    for resultado in resultados:
        assert resultado.nombre is not None
        assert isinstance(resultado.especialidad, int)
