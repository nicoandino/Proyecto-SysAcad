import os
import sys
import random
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

# --- Bootstrap path del proyecto ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app, db
from app.models.facultad import Facultad
from app.models.universidad import Universidad

XML_PATH = "archivados_xml/facultades.xml"

def importar_facultades():
    app = create_app()
    with app.app_context():
        tree = ET.parse(XML_PATH)
        root = tree.getroot()

        # Obtener todas las universidades disponibles
        uni_ids = [u.id for u in Universidad.query.all()]

        for item in root.findall('_expxml'):
            fac_id = int(item.find('facultad').text)
            nombre = item.find('nombre').text.strip()

            nueva = Facultad(
                id=fac_id,
                nombre=nombre,
                universidad_id=random.choice(uni_ids)  # asignación aleatoria
            )
            db.session.add(nueva)

        db.session.commit()
        print("Facultades importadas.")

if __name__ == "__main__":
    importar_facultades()
