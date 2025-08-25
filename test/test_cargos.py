import os
import unittest
from xml.etree import ElementTree as ET

from app import create_app, db
from app.models.cargo import Cargo  # <-- usamos el modelo real

class XMLImportTestCase(unittest.TestCase):
    def setUp(self):
        # Config de test
        os.environ['FLASK_CONTEXT'] = 'testing'
        os.environ['TEST_DATABASE_URI'] = 'postgresql+psycopg2://matuu:matu@localhost:5432/test_sysacad'

        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_import_xml_to_db(self):
        # Ruta del XML de grados (lo usamos para poblar cargos)
        xml_file_path = os.path.join(
            os.path.dirname(__file__), '..', 'archivados_xml', 'grados.xml'
        )
        self.assertTrue(os.path.exists(xml_file_path), f"El archivo {xml_file_path} no existe.")

        # Parseo
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        inserted = 0

        # En tu XML los ítems son <_expxml> con hijos <grado> y <nombre>
        for item in root.findall('_expxml'):
            grado_el = item.find('grado')
            nombre_el = item.find('nombre')

            if grado_el is None or nombre_el is None:
                # faltan datos, lo salteamos
                continue

            nombre = (nombre_el.text or "").strip()
            grado_txt = (grado_el.text or "").strip()
            if not nombre or not grado_txt:
                continue

            try:
                grado = int(grado_txt)
            except ValueError:
                # grado no convertible a entero
                continue

            # Creamos Cargo. La descripcion la cubrirá el modelo con "Sin descripción"
            cargo = Cargo(
                nombre=nombre,
                grado=grado,          # <-- asegurate que Cargo tenga esta columna
                descripcion=None      # <-- el modelo lo transforma a "Sin descripción"
            )
            db.session.add(cargo)
            inserted += 1

        # Commit UNA sola vez
        db.session.commit()

        # Aserciones
        self.assertGreater(inserted, 0, "No se preparó ningún cargo para insertar.")
        count = db.session.query(Cargo).count()
        self.assertEqual(count, inserted, "La cantidad insertada no coincide con lo esperado.")

        # (Opcional) chequear que descripcion nunca quedó NULL
        null_desc = db.session.query(Cargo).filter(Cargo.descripcion.is_(None)).count()
        self.assertEqual(null_desc, 0, "Hay cargos con descripcion NULL y no debería.")

if __name__ == '__main__':
    unittest.main()
