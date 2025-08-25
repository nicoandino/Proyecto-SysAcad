import os
import csv
import unittest
from datetime import date
from app import create_app, db
from app.models.alumno import Alumno

CSV_FILE = "alumnos_test.csv"

class ImportCSVAlumnosTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # App en modo test con SQLite en memoria
        cls.app = create_app()
        cls.app.config.update({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        })
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        """Crear un CSV temporal con 3 alumnos"""
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "apellido", "nombre", "nro_documento", "tipo_documento",
                "fecha_nacimiento", "sexo", "nro_legajo", "fecha_ingreso"
            ])
            writer.writerow(["Pérez", "Juan", 12345678, "DNI", "2000-01-01", "M", 100, "2020-01-01"])
            writer.writerow(["Gómez", "Ana", 87654321, "DNI", "1999-05-10", "F", 101, "2019-03-15"])
            writer.writerow(["López", "María", 11223344, "DNI", "2001-07-20", "F", 102, "2021-02-10"])

    def tearDown(self):
        """Eliminar el archivo CSV después de cada test"""
        if os.path.exists(CSV_FILE):
            os.remove(CSV_FILE)

    def test_importar_csv_a_bd(self):
        """Importa alumnos desde CSV, verifica en BD y borra archivo"""

        # Leer CSV e insertar en la BD
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                alumno = Alumno(
                    apellido=row["apellido"],
                    nombre=row["nombre"],
                    nro_documento=int(row["nro_documento"]),
                    tipo_documento=row["tipo_documento"],
                    fecha_nacimiento=date.fromisoformat(row["fecha_nacimiento"]),
                    sexo=row["sexo"],
                    nro_legajo=int(row["nro_legajo"]),
                    fecha_ingreso=date.fromisoformat(row["fecha_ingreso"])
                )
                db.session.add(alumno)
            db.session.commit()

        # Verificar que los alumnos fueron insertados
        alumnos = db.session.query(Alumno).all()
        self.assertEqual(len(alumnos), 3)
        nombres = sorted([a.nombre for a in alumnos])
        self.assertEqual(nombres, ["Ana", "Juan", "María"])

        # Verificar que el CSV todavía existe (lo borra tearDown)
        self.assertTrue(os.path.exists(CSV_FILE))
