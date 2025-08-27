# test/test_con_model.py
import os
import sys
import pytest
from xml.etree import ElementTree as ET

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ['FLASK_CONTEXT'] = 'testing'
#os.environ['TEST_DATABASE_URI'] = 'sqlite:///:memory:' # Base de datos en memoria

from app import create_app, db
from app.models.facultad import Facultad

@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_importar_facultades(app):
    xml_file_path = os.path.join(BASE_DIR, 'archivados_xml', 'facultades.xml')
    assert os.path.exists(xml_file_path), f"XML no encontrado: {xml_file_path}"

    with open(xml_file_path, 'r', encoding='windows-1252') as f:
        tree = ET.parse(f)
    root = tree.getroot()

    registros_importados = 0
    with app.app_context():
        for item in root.findall('_expxml'):
            nombre_valor = item.findtext('nombre')
            if not nombre_valor:
                continue

            nueva_facultad = Facultad(
                nombre=nombre_valor,
                abreviatura=item.findtext('abreviatura'),
                directorio=item.findtext('directorio'),
                sigla=item.findtext('sigla'),
                codigo_postal=item.findtext('codigo_postal'),
                ciudad=item.findtext('ciudad'),
                domicilio=item.findtext('domicilio'),
                telefono=item.findtext('telefono'),
                contacto=item.findtext('contacto'),
                email=item.findtext('email'),
                codigo=item.findtext('codigo')
            )

            db.session.add(nueva_facultad)
            registros_importados += 1

        db.session.commit()

        total = db.session.query(Facultad).count()
        assert total >= registros_importados, "No se insertaron registros correctamente"
