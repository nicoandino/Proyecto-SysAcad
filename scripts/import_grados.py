import os
import sys
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app, db
from app.models.grado import Grado

XML_RELATIVE_PATH = os.path.join('archivados_xml', 'grados.xml')


def clean(text, maxlen=None, default=None):
    if text is None:
        return default
    s = text.strip()
    if not s:
        return default
    return s[:maxlen] if maxlen else s


def get_text(elem):
    return elem.text if elem is not None else None


def importar_grados():
    #os.environ['FLASK_CONTEXT'] = 'development'
    app = create_app()
    with app.app_context():
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
                grado_id_txt = clean(get_text(item.find('grado')))
                nombre       = clean(get_text(item.find('nombre')), 50)
                descripcion  = clean(get_text(item.find('descripcion')), 200, default="-")  # <- default

                if not grado_id_txt or not nombre:
                    errores += 1
                    continue

                grado_id = int(grado_id_txt)

                if db.session.get(Grado, grado_id):
                    duplicados += 1
                    continue

                nuevo = Grado(
                    id=grado_id,
                    nombre=nombre,
                    descripcion=descripcion
                )

                db.session.add(nuevo)
                db.session.commit()
                insertados += 1

            except ValueError:
                db.session.rollback()
                print(f"Error: 'grado' no es un entero válido: {grado_id_txt}")
                errores += 1
            except IntegrityError as e:
                db.session.rollback()
                print(f"Error de integridad al insertar ID {grado_id_txt}: {e.orig}")
                errores += 1
            except Exception as e:
                db.session.rollback()
                print(f"Error procesando item (ID {grado_id_txt}): {e}")
                errores += 1

        print(f"""
Importación finalizada:
- Registros insertados: {insertados}
- Registros duplicados: {duplicados}
- Registros con error: {errores}
""")


if __name__ == '__main__':
    importar_grados()
