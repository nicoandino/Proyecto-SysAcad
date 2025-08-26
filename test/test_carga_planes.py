import pytest
from xml.etree import ElementTree as ET
from app import create_app, db
from app.models import plan as plan_model
from test.instancias import nuevoplan
import os

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_carga_planes_desde_xml(app_context):
    xml_file_path = os.path.join(
        os.path.dirname(__file__), '..', 'archivados_xml', 'planes.xml'
    )

    assert os.path.exists(xml_file_path), f"El archivo {xml_file_path} no existe."

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    for item in root.findall('_expxml'):
        especialidad_element = item.find('especialidad')
        plan_element = item.find('plan')
        nombre_element = item.find('nombre')

        if especialidad_element is not None and plan_element is not None:
            try:
                especialidad = especialidad_element.text.strip()
                plan = int(plan_element.text.strip())
                nombre = nombre_element.text.strip() if nombre_element is not None else "no definido"

                obj = nuevoplan(especialidad=especialidad, plan=plan, nombre=nombre)
                db.session.add(obj)
            except Exception as e:
                print(f"Error al procesar item: {ET.tostring(item, encoding='unicode')}\n{e}")
        else:
            print(f"Item omitido por datos faltantes: {ET.tostring(item, encoding='unicode')}")

    db.session.commit()

    resultados = plan_model.Plan.query.all()
    assert len(resultados) > 0, "No se insertaron datos en la base de datos."
    for resultado in resultados:
        assert resultado.especialidad is not None
        assert isinstance(resultado.plan, int)
