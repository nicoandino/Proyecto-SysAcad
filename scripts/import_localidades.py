import os
import sys
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError

# --- Bootstrap path del proyecto ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app, db
from app.models.localidad import Localidad  # <-- usamos el modelo existente

XML_RELATIVE_PATH = os.path.join('archivados_xml', 'localidades.xml')


def get_text(elem):
    """Devuelve texto limpio o None."""
    return elem.text.strip() if (elem is not None and elem.text) else None


def importar_localidades():
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

        for item in root.findall('_exportar'):
            try:
                codigo_txt = get_text(item.find('codigo'))
                ciudad = get_text(item.find('ciudad'))
                provincia = get_text(item.find('provincia'))
                pais = get_text(item.find('pais_del_c'))  # según tu XML

                if not codigo_txt or not ciudad:
                    print("Saltado: faltan 'codigo' o 'ciudad'.")
                    errores += 1
                    continue

                codigo = int(codigo_txt)

                # Evitar duplicados por PK (usamos que id=codigo)
                if Localidad.query.get(codigo):
                    print(f"Duplicado ID {codigo}: {ciudad}")
                    duplicados += 1
                    continue

                nueva = Localidad(
                    id=codigo,        # PK = código (como en tu importador original)
                    codigo=codigo,
                    ciudad=ciudad,
                    provincia=provincia,
                    pais=pais
                )

                db.session.add(nueva)
                db.session.commit()
                insertados += 1

            except ValueError:
                db.session.rollback()
                print(f"Error: 'codigo' no es un entero válido: {codigo_txt}")
                errores += 1
            except IntegrityError:
                db.session.rollback()
                print(f"Error de integridad al insertar ID {codigo_txt}")
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
    importar_localidades()
