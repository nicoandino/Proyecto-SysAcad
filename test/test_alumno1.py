import unittest
import os
from flask import current_app
from app import create_app
from datetime import date
from app.models.tipodocumento import TipoDocumento
from app.models.alumno import Alumno
from app.services import AlumnoService
from app.services import TipoDocumentoService
from test.instancias import nuevoalumno, nuevotipodocumento
from app import db

class AlumnoTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_crear(self):
        alumno = nuevoalumno()
        self.assertIsNotNone(alumno)
        self.assertIsNotNone(alumno.nombre)
        self.assertGreaterEqual(alumno.id, 1)
        self.assertEqual(alumno.apellido, "Pérez")
    def test_buscar_por_id(self):
        alumno = nuevoalumno()
        db.session.add(alumno)
        db.session.commit()   # acá se asigna el ID real

        r = AlumnoService.buscar_por_id(alumno.id)

        self.assertIsNotNone(r)
        self.assertEqual(r.nombre, "Juan")
        self.assertEqual(r.apellido, "Pérez")

    def test_buscar_todos(self):
        alumno1 = nuevoalumno()
        db.session.add(alumno1)

        tipo_doc2 = nuevotipodocumento()
        db.session.add(tipo_doc2)
        db.session.commit()   # 👈 importante
        alumno2 = nuevoalumno(
            nombre="Pedro",
            apellido="Gómez",
            nro_documento=12345678,
            tipo_documento="Pasaporte",   # 👈 string
            fecha_nacimiento=date(1995,5,5),
            sexo="M",
            nro_legajo=654321,
            fecha_ingreso=date(2021,1,1)
        )

        db.session.add(alumno2)
        db.session.commit()


        alumnos = AlumnoService.buscar_todos()
        self.assertIsNotNone(alumnos)
        self.assertEqual(len(alumnos), 2)

    def test_actualizar(self):
        alumno = nuevoalumno()
        db.session.add(alumno)
        db.session.commit()

        alumno.nombre = "Juan actualizado"
        alumno_actualizado = AlumnoService.actualizar(alumno.id, alumno)

        self.assertIsNotNone(alumno_actualizado)
        self.assertEqual(alumno_actualizado.nombre, "Juan actualizado")

    def test_borrar(self):
        alumno = nuevoalumno()
        db.session.add(alumno)
        db.session.commit()

        borrado = AlumnoService.borrar_por_id(alumno.id)
        self.assertTrue(borrado)
