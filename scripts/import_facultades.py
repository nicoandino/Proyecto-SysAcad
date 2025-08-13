import os
import sys
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError

# --- Bootstrap path del proyecto ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app, db
from app.models.facultad import Facultad

XML_RELATIVE_PATH = os.path.join('archivados_xml', 'facultades.xml')


def get_text(elem):
    """Texto limpio o None."""
    return elem.text.strip() if (elem is not None and elem.text) else None


def importar_facultades():
    # Contexto Flask (ajústalo si corresponde)
    #os.environ['FLASK_CONTEXT'] = 'development'

    app = create_app()
    with app.app_context():
        db.create_all()

        xml_file_path = os.path.abspath(os.path.join(BASE_DIR, XML_RELATIVE_PATH))
        if not os.path.exists(xml_file_path):
            print(f"ERROR: No se encontró el archivo XML: {xml_file_path}")
            return

        print(f"Importando desde: {xml_file_path}")

        # ET.parse respeta la codificación declarada en la cabecera del XML
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
                facultad_id_txt = get_text(item.find('facultad'))
                nombre = get_text(item.find('nombre'))
                abreviatura = get_text(item.find('abreviatura'))
                directorio = get_text(item.find('directorio'))
                sigla = get_text(item.find('sigla'))
                codigo_postal = get_text(item.find('codigo_postal'))
                ciudad = get_text(item.find('ciudad'))
                domicilio = get_text(item.find('domicilio'))
                telefono = get_text(item.find('telefono'))
                contacto = get_text(item.find('contacto'))
                email = get_text(item.find('email'))
                codigo = get_text(item.find('codigo'))

                if not facultad_id_txt or not nombre:
                    print("Saltado: faltan 'facultad' o 'nombre'.")
                    errores += 1
                    continue

                facultad_id = int(facultad_id_txt)

                # Evitar duplicados por PK
                if Facultad.query.get(facultad_id):
                    print(f"Duplicado ID {facultad_id}: {nombre}")
                    duplicados += 1
                    continue

                nueva = Facultad(
                    id=facultad_id,
                    nombre=nombre,
                    abreviatura=abreviatura,
                    directorio=directorio,
                    sigla=sigla,
                    codigo_postal=codigo_postal,
                    ciudad=ciudad,
                    domicilio=domicilio,
                    telefono=telefono,
                    contacto=contacto,
                    email=email,
                    codigo=codigo
                )

                db.session.add(nueva)
                db.session.commit()
                insertados += 1

            except ValueError:
                db.session.rollback()
                print(f"Error: 'facultad' no es un entero válido: {facultad_id_txt}")
                errores += 1
            except IntegrityError:
                db.session.rollback()
                print(f"Error de integridad al insertar ID {facultad_id_txt}")
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
    importar_facultades()
