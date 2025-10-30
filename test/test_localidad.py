import unittest
from app import create_app, db
from app.models import Localidad
from app.services import LocalidadService
from test.instancias import nuevalocalidad


class LocalidadTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Limpia la base de datos al finalizar cada test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_crear_localidad(self):
        loc = Localidad(codigo=2000, ciudad="Godoy Cruz", provincia="Mendoza", pais="Argentina")
        LocalidadService.crear(loc)

        self.assertIsNotNone(loc.id)
        self.assertEqual(loc.ciudad, "Godoy Cruz")
        self.assertEqual(loc.codigo, 2000)

    def test_buscar_por_id(self):
        loc = nuevalocalidad(ciudad="Luján de Cuyo", codigo=5507)
        encontrada = LocalidadService.buscar_por_id(loc.id)

        self.assertIsNotNone(encontrada)
        self.assertEqual(encontrada.ciudad, "Luján de Cuyo")
        self.assertEqual(encontrada.codigo, 5507)

    def test_buscar_todos(self):
        nuevalocalidad(ciudad="San Rafael")
        nuevalocalidad(ciudad="Malargüe")
        localidades = LocalidadService.buscar_todos()

        self.assertGreaterEqual(len(localidades), 2)
        nombres = [l.ciudad for l in localidades]
        self.assertIn("San Rafael", nombres)
        self.assertIn("Malargüe", nombres)

    def test_actualizar_localidad(self):
        loc = nuevalocalidad(ciudad="Tunuyán", codigo=5560)
        loc.ciudad = "Tunuyán Centro"
        loc.provincia = "Mendoza"
        actualizada = LocalidadService.actualizar(loc.id, loc)

        self.assertEqual(actualizada.ciudad, "Tunuyán Centro")
        self.assertEqual(actualizada.provincia, "Mendoza")

    def test_borrar_localidad(self):
        loc = nuevalocalidad(ciudad="Lavalle")
        borrada = LocalidadService.borrar_por_id(loc.id)

        self.assertTrue(borrada)
        resultado = LocalidadService.buscar_por_id(loc.id)
        self.assertIsNone(resultado)
