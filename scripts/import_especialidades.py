import os
import sys
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app, db
from app.models.especialidad import Especialidad

XML_RELATIVE_PATH = os.path.join('archivados_xml', 'especialidades.xml')


def get_text(elem):
    """Devuelve el texto limpio de un elemento o None."""
    return elem.text.strip() if (elem is not None and elem.text) else None


def importar_especialidades():
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
                especialidad_id_text = get_text(item.find('especialidad'))
                nombre = get_text(item.find('nombre'))
                letra = get_text(item.find('letra')) or None
                observacion = get_text(item.find('observacion'))

                if not especialidad_id_text or not nombre:
                    print("Saltado: faltan 'especialidad' o 'nombre'.")
                    errores += 1
                    continue

                especialidad_id = int(especialidad_id_text)

                if db.session.get(Especialidad, especialidad_id):
                    print(f"Duplicado ID {especialidad_id}: {nombre}")
                    duplicados += 1
                    continue

                nueva = Especialidad(
                    id=especialidad_id,
                    nombre=nombre,
                    letra=letra,
                    observacion=observacion,
                    tipoespecialidad_id=None,
                    facultad_id=None
                )
                db.session.add(nueva)
                db.session.commit()
                insertados += 1

            except ValueError:
                db.session.rollback()
                print(f"Error: 'especialidad' no es un entero válido: {repr(especialidad_id_text)}")
                errores += 1
            except IntegrityError as e:
                db.session.rollback()
                print(f"Error de integridad al insertar ID {repr(especialidad_id_text)}: {e.orig}")
                errores += 1
            except Exception as e:
                db.session.rollback()
                print(f"Error procesando item (ID {repr(especialidad_id_text)}): {e}")
                errores += 1

        print(f"""
Importación finalizada:
- Registros insertados: {insertados}
- Registros duplicados: {duplicados}
- Registros con error: {errores}
""")


if __name__ == '__main__':
    importar_especialidades()
