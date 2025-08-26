import pytest
from xml.etree import ElementTree as ET
from app import create_app, db
from app.models import orientacion as orientacion_model
from test.instancias import nuevaorientacion
import os

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_carga_orientaciones_desde_xml(app_context):
    xml_file_path = os.path.join(
        os.path.dirname(__file__), '..', 'archivados_xml', 'orientaciones.xml'
    )

    assert os.path.exists(xml_file_path), f"El archivo {xml_file_path} no existe."

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    for item in root.findall('_expxml'):
        especialidad_element = item.find('especialidad')
        plan_element = item.find('plan')
        orientacion_element = item.find('orientacion')
        nombre_element = item.find('nombre')

        if all([especialidad_element, plan_element, orientacion_element, nombre_element]):
            especialidad = especialidad_element.text.strip()
            plan = plan_element.text.strip()
            orientacion = orientacion_element.text.strip()
            nombre = nombre_element.text.strip()

            obj = nuevaorientacion(
                especialidad=especialidad,
                plan=plan,
                orientacion=orientacion,
                nombre=nombre
            )
            db.session.add(obj)
        else:
            print(f"Item omitido por datos faltantes: {ET.tostring(item, encoding='unicode')}")

    db.session.commit()

    resultados = orientacion_model.Orientacion.query.all()
    assert len(resultados) > 0, "No se insertaron datos en la base de datos."
    for resultado in resultados:
        assert resultado.nombre is not None
        assert resultado.orientacion is not None
        assert resultado.plan is not None
