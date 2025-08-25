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
from app.models.plan import Plan                # ← si tu modelo está en otro módulo, ajusta el import
from app.models.orientacion import Orientacion  # usamos el modelo existente

XML_RELATIVE_PATH = os.path.join('archivados_xml', 'orientaciones.xml')


def get_text(elem):
    return elem.text.strip() if (elem is not None and elem.text) else None


def to_int(text):
    try:
        return int(text) if text not in (None, "") else None
    except ValueError:
        return None


def importar_orientaciones():
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
                plan_id = to_int(get_text(item.find('plan')))       # ← renombrado a plan_id
                nombre = get_text(item.find('nombre'))

                if especialidad_id is None or plan_id is None:
                    print("Saltado: faltan 'especialidad' o 'plan'.")
                    errores += 1
                    continue

                # Validar FK: la especialidad debe existir
                if not Especialidad.query.get(especialidad_id):
                    print(f"Error: especialidad ID {especialidad_id} no existe. Saltando registro.")
                    errores += 1
                    continue

                # (Opcional) Validar que exista el Plan
                if not Plan.query.get(plan_id):
                    print(f"Error: plan ID {plan_id} no existe. Saltando registro.")
                    errores += 1
                    continue

                # Evitar duplicados por (especialidad_id, plan_id)
                existing = Orientacion.query.filter_by(
                    especialidad_id=especialidad_id,
                    plan_id=plan_id                                # ← usar la FK, no la relación
                ).first()

                if existing:
                    print(f"Duplicado: Esp {especialidad_id}, Plan {plan_id}, Nombre: {nombre}")
                    duplicados += 1
                    continue

                nueva = Orientacion(
                    especialidad_id=especialidad_id,
                    plan_id=plan_id,                               # ← usar plan_id
                    nombre=nombre
                )

                db.session.add(nueva)
                db.session.commit()
                insertados += 1
                print(f"Guardado Orientación ID {nueva.id}: Esp {especialidad_id}, Plan {plan_id}, Nombre: {nombre}")

            except IntegrityError:
                db.session.rollback()
                print(f"Error de integridad al insertar Esp {especialidad_id}, Plan {plan_id}")
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
    importar_orientaciones()
