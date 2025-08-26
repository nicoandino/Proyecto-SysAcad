import pytest
from xml.etree import ElementTree as ET
from app import create_app, db
from app.models import cargo as cargo_model
from test.instancias import nuevacargo
import os

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_carga_cargos_desde_xml(app_context):
    xml_file_path = os.path.join(
        os.path.dirname(__file__), '..', 'archivados_xml', 'grados.xml'
    )
    assert os.path.exists(xml_file_path), f"El archivo {xml_file_path} no existe."

    with open(xml_file_path, 'r', encoding='windows-1252') as f:
        tree = ET.parse(f)
    root = tree.getroot()

    inserted = 0

    for item in root.findall('_expxml'):
        grado_el = item.find('grado')
        nombre_el = item.find('nombre')

        if grado_el is None or nombre_el is None:
            continue

        nombre = (nombre_el.text or "").strip()
        grado_txt = (grado_el.text or "").strip()
        if not nombre or not grado_txt:
            continue

        try:
            grado = int(grado_txt)
        except ValueError:
            continue

        cargo = nuevacargo(nombre=nombre, grado=grado, descripcion="Sin descripción")
        db.session.add(cargo)
        inserted += 1

    db.session.commit()

    resultados = cargo_model.Cargo.query.all()
    assert inserted > 0, "No se preparó ningún cargo para insertar."
    assert len(resultados) == inserted, f"Se esperaban {inserted} cargos, pero hay {len(resultados)}."

    sin_descripcion = [c for c in resultados if c.descripcion is None]
    assert len(sin_descripcion) == 0, "Hay cargos con descripción NULL y no debería."
