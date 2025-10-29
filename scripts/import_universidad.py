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

def clean(t, n=None):
    if t is None: return None
    s = t.strip()
    if not s: return None
    return s[:n] if n else s

def txt(e): return e.text if e is not None else None

def importar_universidades():
    app = create_app()
    with app.app_context():
        path = os.path.abspath(os.path.join(BASE_DIR, XML_RELATIVE_PATH))
        tree = ET.parse(path); root = tree.getroot()

        ins = dup = err = 0
        for item in root.findall('_expxml'):
            uni_id_txt = clean(txt(item.find('universida'))) or clean(txt(item.find('universidad')))
            nombre = clean(txt(item.find('nombre')), 255)
            sigla  = clean(txt(item.find('sigla')), 50)

            if not uni_id_txt or not nombre:
                err += 1; continue

            try:
                uni_id = int(uni_id_txt)
                if db.session.get(Universidad, uni_id):
                    dup += 1; continue

                db.session.add(Universidad(id=uni_id, nombre=nombre, sigla=sigla))
                db.session.commit(); ins += 1
            except (ValueError, IntegrityError) as e:
                db.session.rollback(); err += 1; print("Error:", e)

        print(f"Universidades -> insertadas: {ins}, duplicadas: {dup}, errores: {err}")

if __name__ == "__main__":
    importar_universidades()
