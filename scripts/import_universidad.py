# scripts/importar_universidades.py
import os
import sys
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

# --- Bootstrap path del proyecto ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app, db
from app.models.universidad import Universidad

XML_RELATIVE_PATH = os.path.join('archivados_xml', 'universidad.xml')


def get_text(elem):
    """Devuelve texto limpio o None."""
    return elem.text.strip() if (elem is not None and elem.text) else None


def get_first_text(parent, *tags):
    """Devuelve el texto del primer tag existente en parent (o None)."""
    for t in tags:
        v = parent.find(t)
        if v is not None and v.text:
            return v.text.strip()
    return None


def importar_universidades():
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
            tree = ET.parse(xml_file_path)  # respeta la codificación del XML
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"Error al parsear el archivo XML: {e}")
            return

        insertados = 0
        duplicados = 0
        errores = 0

        for item in root.findall('_expxml'):
            try:
                universidad_id_txt = get_first_text(item, 'universida', 'universidad')
                nombre = get_text(item.find('nombre')) or ''
                sigla = get_text(item.find('sigla'))

                if not universidad_id_txt or not nombre:
                    print("Saltado: faltan 'universidad' (id) o 'nombre'.")
                    errores += 1
                    continue

                # Parseo y saneo de campos
                universidad_id = int(universidad_id_txt)
                nombre = nombre.strip()[:100]
                sigla = (sigla or '-').strip()[:10]  # default si no viene en el XML

                # Evitar duplicados por PK
                if Universidad.query.get(universidad_id):
                    print(f"Duplicado ID {universidad_id}: {nombre}")
                    duplicados += 1
                    continue

                nueva = Universidad(
                    id=universidad_id,  # cargamos el ID legado del XML
                    nombre=nombre,
                    sigla=sigla
                )

                db.session.add(nueva)
                db.session.commit()
                insertados += 1

            except ValueError:
                db.session.rollback()
                print(f"Error: 'universidad' no es un entero válido: {universidad_id_txt}")
                errores += 1
            except IntegrityError as ie:
                db.session.rollback()
                print(f"Error de integridad al insertar ID {universidad_id_txt}: {ie}")
                errores += 1
            except Exception as e:
                db.session.rollback()
                print(f"Error procesando item: {e}")
                errores += 1

        # --- Reseteo de secuencia por haber seteado IDs manualmente ---
        try:
            db.session.execute(text("""
                SELECT setval(
                  pg_get_serial_sequence('universidades','id'),
                  COALESCE((SELECT MAX(id) FROM universidades), 1)
                )
            """))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Advertencia: no se pudo ajustar la secuencia de 'universidades': {e}")

        print(f"""
Importación finalizada:
- Registros insertados: {insertados}
- Registros duplicados: {duplicados}
- Registros con error: {errores}
""")


if __name__ == '__main__':
    importar_universidades()
