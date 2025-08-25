import os
import sys
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app, db
from app.models.materia import Materia

XML_RELATIVE_PATH = os.path.join('archivados_xml', 'materias.xml')


def clean(text, maxlen=None):
    if text is None:
        return None
    s = text.strip()
    if not s:
        return None
    return s[:maxlen] if maxlen else s


def get_text(elem):
    return elem.text if elem is not None else None


def importar_materias():
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
                materia_id_txt = clean(get_text(item.find('materia')))
                nombre = clean(get_text(item.find('nombre')), 255)

                # Si tu XML no tiene <codigo>, podés derivarlo del mismo id como string
                # o dejarlo None:
                codigo = clean(get_text(item.find('codigo')), 20) or (
                    str(materia_id_txt) if materia_id_txt else None
                )
                observacion = clean(get_text(item.find('observacion')), 255)

                if not materia_id_txt or not nombre:
                    errores += 1
                    continue

                materia_id = int(materia_id_txt)

                # Duplicado por PK (SQLAlchemy 2.x)
                if db.session.get(Materia, materia_id):
                    duplicados += 1
                    continue

                nueva = Materia(
                    id=materia_id,
                    nombre=nombre,
                    codigo=codigo,
                    observacion=observacion
                )

                db.session.add(nueva)
                db.session.commit()
                insertados += 1

            except ValueError:
                db.session.rollback()
                print(f"Error: 'materia' no es un entero válido: {materia_id_txt}")
                errores += 1
            except IntegrityError as e:
                db.session.rollback()
                print(f"Error de integridad al insertar ID {materia_id_txt}: {getattr(e, 'orig', e)}")
                errores += 1
            except Exception as e:
                db.session.rollback()
                print(f"Error procesando item (ID {materia_id_txt}): {e}")
                errores += 1

        print(f"""
Importación finalizada:
- Registros insertados: {insertados}
- Registros duplicados: {duplicados}
- Registros con error: {errores}
""")


if __name__ == '__main__':
    importar_materias()
