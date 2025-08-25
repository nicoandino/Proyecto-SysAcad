import unittest
from app import create_app, db
from app.models.alumno import Alumno
from datetime import date

class CertificadoTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Crear app en modo TEST con SQLite en memoria
        cls.app = create_app()
        cls.app.config.update({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        })
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # Crear tablas
        db.create_all()

        # Insertar un alumno de prueba (usando los nombres reales de columnas)
        alumno = Alumno(
            apellido="Pérez",
            nombre="Juan",
            nro_documento=12345678,        # 👈 columna real
            tipo_documento="DNI",          # 👈 columna real
            fecha_nacimiento=date(2000,1,1),
            sexo="M",
            nro_legajo=100,                # 👈 PK
            fecha_ingreso=date(2020,1,1)
        )
        db.session.add(alumno)
        db.session.commit()

        cls.nro_legajo = alumno.nro_legajo

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_certificado(self):
        client = self.app.test_client()
        response = client.get(f"/api/v1/certificado/{self.nro_legajo}/docx")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.mimetype,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        self.assertGreater(len(response.data), 1000, "El certificado generado está vacío o corrupto")
