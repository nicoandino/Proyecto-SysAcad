import pytest
from xml.etree import ElementTree as ET
from app import create_app, db
from app.models import universidad as universidad_model
from test.instancias import nuevauniversidad
import os

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_carga_universidades_desde_xml(app_context):
    xml_file_path = os.path.join(
        os.path.dirname(__file__), '..', 'archivados_xml', 'universidad.xml'
    )

    assert os.path.exists(xml_file_path), f"El archivo {xml_file_path} no existe."

    with open(xml_file_path, 'r', encoding='windows-1252') as f:
        tree = ET.parse(f)
    root = tree.getroot()

    for item in root.findall('_expxml'):
        nombre_element = item.find('nombre')

        if nombre_element is not None and nombre_element.text:
            nombre = nombre_element.text.strip()
            obj = nuevauniversidad(nombre=nombre)
            db.session.add(obj)
        else:
            print(f"Item omitido por falta de nombre: {ET.tostring(item, encoding='unicode')}")

    db.session.commit()

    resultados = universidad_model.Universidad.query.all()
    assert len(resultados) > 0, "No se insertaron datos en la base de datos."
    for resultado in resultados:
        assert resultado.nombre is not None
