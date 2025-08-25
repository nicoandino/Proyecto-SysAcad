import os
import sys
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app, db
from app.models.facultad import Facultad

XML_RELATIVE_PATH = os.path.join('archivados_xml', 'facultades.xml')


def clean(text, maxlen=None):
    if text is None:
        return None
    s = text.strip()
    if not s:
        return None
    return s[:maxlen] if maxlen else s


def get_text(elem):
    return elem.text if elem is not None else None


def importar_facultades():
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
                facultad_id_txt = clean(get_text(item.find('facultad')))
                nombre         = clean(get_text(item.find('nombre')),        100)
                abreviatura    = clean(get_text(item.find('abreviatura')),   10)
                directorio     = clean(get_text(item.find('directorio')),   100)
                sigla          = clean(get_text(item.find('sigla')),         10)
                codigopostal   = clean(get_text(item.find('codigopostal')),  10)
                ciudad         = clean(get_text(item.find('ciudad')),        50)
                domicilio      = clean(get_text(item.find('domicilio')),    100)
                telefono       = clean(get_text(item.find('telefono')),      20)
                contacto       = clean(get_text(item.find('contacto')),     100)
                email          = clean(get_text(item.find('email')),        100)

                if not facultad_id_txt or not nombre:
                    errores += 1
                    continue

                facultad_id = int(facultad_id_txt)

                if db.session.get(Facultad, facultad_id):
                    duplicados += 1
                    continue

                nueva = Facultad(
                    id=facultad_id,
                    nombre=nombre,
                    abreviatura=abreviatura,
                    directorio=directorio,
                    sigla=sigla,
                    codigopostal=codigopostal,
                    ciudad=ciudad,
                    domicilio=domicilio,
                    telefono=telefono,
                    contacto=contacto,
                    email=email,
                )

                db.session.add(nueva)
                db.session.commit()
                insertados += 1

            except ValueError:
                db.session.rollback()
                print(f"Error: 'facultad' no es un entero válido: {facultad_id_txt}")
                errores += 1
            except IntegrityError as e:
                db.session.rollback()
                print(f"Error de integridad al insertar ID {facultad_id_txt}: {e.orig}")
                errores += 1
            except Exception as e:
                db.session.rollback()
                print(f"Error procesando item (ID {facultad_id_txt}): {e}")
                errores += 1

        print(f"""
Importación finalizada:
- Registros insertados: {insertados}
- Registros duplicados: {duplicados}
- Registros con error: {errores}
""")


if __name__ == '__main__':
    importar_facultades()
