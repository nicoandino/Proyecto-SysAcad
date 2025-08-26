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

def test_con_model_importar_facultades(app_context):
    xml_file_path = os.path.join(
        os.path.dirname(__file__), '..', 'archivados_xml', 'facultades.xml'
    )
    assert os.path.exists(xml_file_path), f"XML no encontrado: {xml_file_path}"

    with open(xml_file_path, 'r', encoding='windows-1252') as f:
        tree = ET.parse(f)
    root = tree.getroot()

    registros_importados = 0

    for item in root.findall('_expxml'):
        nombre = item.findtext('nombre')
        if not nombre:
            continue

        facultad = nuevafacultad(
            nombre=nombre.strip(),
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

        db.session.add(facultad)
        registros_importados += 1

    db.session.commit()

    total = facultad_model.Facultad.query.count()
    assert total >= registros_importados, "No se insertaron registros correctamente"
