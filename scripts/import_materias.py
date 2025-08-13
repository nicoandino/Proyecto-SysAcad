import os
import sys
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError

# --- Bootstrap path del proyecto ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app, db
from app.models.materia import Materia

XML_RELATIVE_PATH = os.path.join('archivados_xml', 'materias.xml')


def get_text(elem):
    """Devuelve texto limpio o None."""
    return elem.text.strip() if (elem is not None and elem.text) else None


def to_int(text):
    """Convierte a int o devuelve None si no aplica."""
    try:
        return int(text) if text not in (None, "") else None
    except ValueError:
        return None


def importar_materias():
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
            # ET.parse respeta la codificación declarada en la cabecera del XML
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
                materia_id_txt = get_text(item.find('materia'))
                nombre = get_text(item.find('nombre'))

                if not materia_id_txt or not nombre:
                    print("Saltado: faltan 'materia' (id) o 'nombre'.")
                    errores += 1
                    continue

                materia_id = int(materia_id_txt)

                # Campos opcionales
                especialidad = to_int(get_text(item.find('especialidad')))
                plan = to_int(get_text(item.find('plan')))
                materia_code = get_text(item.find('materia'))  # en tu XML suele ser el mismo nodo
                ano = to_int(get_text(item.find('ano')))

                # Evitar duplicados por PK
                if Materia.query.get(materia_id):
                    print(f"Duplicado ID {materia_id}: {nombre}")
                    duplicados += 1
                    continue

                nueva = Materia(
                    id=materia_id,
                    especialidad=especialidad,
                    plan=plan,
                    materia=materia_code,
                    nombre=nombre,
                    ano=ano
                )

                # Mostrar datos antes de guardar (útil para debug)
                print("\n=== Datos a guardar ===")
                print(f"ID: {nueva.id}")
                print(f"Especialidad: {nueva.especialidad}")
                print(f"Plan: {nueva.plan}")
                print(f"Materia (código): {nueva.materia}")
                print(f"Nombre: {nueva.nombre}")
                print(f"Año: {nueva.ano}")
                print("=" * 50)

                db.session.add(nueva)
                db.session.commit()
                insertados += 1

            except ValueError:
                db.session.rollback()
                print(f"Error: 'materia' no es un entero válido: {materia_id_txt}")
                errores += 1
            except IntegrityError:
                db.session.rollback()
                print(f"Error de integridad al insertar ID {materia_id_txt}")
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
    importar_materias()
