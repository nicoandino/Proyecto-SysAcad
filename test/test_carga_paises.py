import pytest
from xml.etree import ElementTree as ET
from app import create_app, db
from app.models import pais as pais_model
from test.instancias import nuevopais
import os

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_carga_paises_desde_xml(app_context):
    xml_file_path = os.path.join(
        os.path.dirname(__file__), '..', 'archivados_xml', 'paises.xml'
    )

    assert os.path.exists(xml_file_path), f"El archivo {xml_file_path} no existe."

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    for item in root.findall('_expxml'):
        pais_element = item.find('pais')
        nombre_element = item.find('nombre')

        if pais_element is not None and nombre_element is not None:
            try:
                pais = int(pais_element.text.strip())
                nombre = nombre_element.text.strip()
                obj = nuevopais(pais=pais, nombre=nombre)
                db.session.add(obj)
            except Exception as e:
                print(f"Error al procesar item: {ET.tostring(item, encoding='unicode')}\n{e}")
        else:
            print(f"Item omitido por datos faltantes: {ET.tostring(item, encoding='unicode')}")

    db.session.commit()

    resultados = pais_model.Pais.query.all()
    assert len(resultados) > 0, "No se insertaron datos en la base de datos."
    for resultado in resultados:
        assert resultado.nombre is not None
        assert isinstance(resultado.pais, int)
