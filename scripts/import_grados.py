import os
import sys
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError

# --- Bootstrap path del proyecto ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app, db
from app.models.grado import Grado

XML_RELATIVE_PATH = os.path.join('archivados_xml', 'grados.xml')


def get_text(elem):
    """Devuelve texto limpio o None."""
    return elem.text.strip() if (elem is not None and elem.text) else None


def importar_grados():
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
                grado_id_txt = get_text(item.find('grado'))
                nombre = get_text(item.find('nombre'))

                if not grado_id_txt or not nombre:
                    print("Saltado: faltan 'grado' o 'nombre'.")
                    errores += 1
                    continue

                grado_id = int(grado_id_txt)

                # Evitar duplicados por PK
                if Grado.query.get(grado_id):
                    print(f"Duplicado ID {grado_id}: {nombre}")
                    duplicados += 1
                    continue

                nuevo = Grado(
                    id=grado_id,
                    nombre=nombre
                )

                db.session.add(nuevo)
                db.session.commit()
                insertados += 1

            except ValueError:
                db.session.rollback()
                print(f"Error: 'grado' no es un entero válido: {grado_id_txt}")
                errores += 1
            except IntegrityError:
                db.session.rollback()
                print(f"Error de integridad al insertar ID {grado_id_txt}")
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
    importar_grados()
