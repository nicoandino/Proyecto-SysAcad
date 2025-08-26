import pytest
from xml.etree import ElementTree as ET
from app import create_app, db
from app.models import materia as materia_model
from test.instancias import nuevamateria
import os

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        yield app

def test_carga_materias_desde_xml(app_context):
    xml_file_path = os.path.join(
        os.path.dirname(__file__), '..', 'archivados_xml', 'materias.xml'
    )

    assert os.path.exists(xml_file_path), f"El archivo {xml_file_path} no existe."

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    for item in root.findall('_expxml'):
        especialidad_element = item.find('especialidad')
        plan_element = item.find('plan')
        materia_element = item.find('materia')
        nombre_element = item.find('nombre')
        ano_element = item.find('ano')

        if all([especialidad_element, plan_element, materia_element, nombre_element]):
            especialidad = especialidad_element.text.strip()
            plan = plan_element.text.strip()
            materia = materia_element.text.strip()
            nombre = nombre_element.text.strip()

            try:
                ano = int(ano_element.text.strip()) if ano_element is not None else None
            except (ValueError, AttributeError):
                ano = None
                print(f"Advertencia: Año inválido para materia {materia}, se establece como None")

            obj = nuevamateria(
                especialidad=especialidad,
                plan=plan,
                materia=materia,
                nombre=nombre,
                ano=ano
            )
            db.session.add(obj)
        else:
            print(f"Item omitido por datos faltantes: {ET.tostring(item, encoding='unicode')}")

    db.session.commit()

    resultados = materia_model.Materia.query.all()
    assert len(resultados) > 0, "No se insertaron datos en la base de datos."
    for resultado in resultados:
        assert resultado.nombre is not None
        assert resultado.plan is not None
        assert resultado.materia is not None
