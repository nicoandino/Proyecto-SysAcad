import pytest
from xml.etree import ElementTree as ET
from app import create_app, db
from app.models import facultad as facultad_model
from test.instancias import nuevafacultad
import os

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_carga_facultades_desde_xml(app_context):
    xml_file_path = os.path.join(
        os.path.dirname(__file__), '..', 'archivados_xml', 'facultades.xml'
    )

    assert os.path.exists(xml_file_path), f"El archivo {xml_file_path} no existe."

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    for item in root.findall('_expxml'):
        facultad_element = item.find('facultad')
        nombre_element = item.find('nombre')

        if facultad_element is not None and nombre_element is not None:
            facultad = int(facultad_element.text)
            nombre = nombre_element.text
            obj = nuevafacultad(facultad=facultad, nombre=nombre)
            db.session.add(obj)
        else:
            print(f"Item omitido por datos faltantes: {ET.tostring(item, encoding='unicode')}")

    db.session.commit()

    resultados = facultad_model.Facultad.query.all()
    assert len(resultados) > 0, "No se insertaron datos en la base de datos."
    for resultado in resultados:
        assert resultado.nombre is not None
        assert isinstance(resultado.facultad, int)
