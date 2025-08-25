# scripts/importar_planes.py
import os
import sys
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError

# --- Bootstrap path del proyecto ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app, db
from app.models.especialidad import Especialidad
from app.models.plan import Plan  # usamos el modelo externo

XML_RELATIVE_PATH = os.path.join('archivados_xml', 'planes.xml')


def get_text(elem):
    """Devuelve texto limpio o None."""
    return elem.text.strip() if (elem is not None and elem.text) else None


def to_int(text):
    """Convierte a int o devuelve None."""
    try:
        return int(text) if text not in (None, "") else None
    except ValueError:
        return None


def importar_planes():
    # Contexto Flask
    #os.environ['FLASK_CONTEXT'] = 'development'

    app = create_app()
    with app.app_context():
        db.create_all()

        xml_file_path = os.path.abspath(os.path.join(BASE_DIR, XML_RELATIVE_PATH))
        if not os.path.exists(xml_file_path):
            print(f"ERROR: No se encontró el archivo XML: {xml_file_path}")
            return

        print(f"Importando desde: {xml_file_path}")

        try:
            # Respeta la codificación declarada en la cabecera del XML
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"Error al parsear el archivo XML: {e}")
            return

        insertados = 0
        duplicados = 0
        errores = 0

        for item in root.findall('_expxml'):
            try:
                especialidad_id = to_int(get_text(item.find('especialidad')))
                plan_num = to_int(get_text(item.find('plan')))
                nombre = get_text(item.find('nombre'))

                if especialidad_id is None or plan_num is None:
                    print("Saltado: faltan 'especialidad' o 'plan'.")
                    errores += 1
                    continue

                # Validar FK: especialidad debe existir
                if not Especialidad.query.get(especialidad_id):
                    print(f"Error: especialidad ID {especialidad_id} no existe. Saltando plan.")
                    errores += 1
                    continue

                # Evitar duplicados por (especialidad_id, plan)
                existing = Plan.query.filter_by(
                    especialidad_id=especialidad_id,
                    anio=plan_num
                ).first()

                if existing:
                    print(f"Duplicado Plan {plan_num} para Especialidad {especialidad_id}: {nombre}")
                    duplicados += 1
                    continue

                nuevo = Plan(
                    especialidad_id=especialidad_id,
                    anio=plan_num,
                    nombre=nombre,
                    fecha_inicio=None,
                    fecha_fin=None,
                    observacion=None
                )

                db.session.add(nuevo)
                db.session.commit()
                insertados += 1
                print(f"Guardado Plan ID {nuevo.id}: Esp {especialidad_id}, Plan {plan_num}, Nombre: {nombre}")

            except IntegrityError:
                db.session.rollback()
                print(f"Error de integridad al insertar Esp {especialidad_id}, Plan {plan_num}")
                errores += 1
            except Exception as e:
                db.session.rollback()
                print(f"Error procesando item: {e}")
                errores += 1

        print(f"""
Importación finalizada:
- Registros insertados: {insertados}
- Registros duplicados: {duplicados}
- Registros con error: {errores}
""")


if __name__ == '__main__':
    importar_planes()
