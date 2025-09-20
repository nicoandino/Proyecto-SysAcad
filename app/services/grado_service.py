# app/services/grado_service.py
from app import db
from app.models import Grado
from app.repositories.grado_repositorio import GradoRepository

class GradoService:

    @staticmethod
    def crear(grado: Grado) -> Grado:
        return GradoRepository.crear(grado)   # devolver instancia

    @staticmethod
    def buscar_por_id(id: int) -> Grado | None:
        return GradoRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[Grado]:
        return GradoRepository.buscar_todos()

    @staticmethod
    def actualizar(id: int, grado: Grado) -> Grado | None:
        existente = GradoRepository.buscar_por_id(id)   # usar el parámetro id
        if not existente:
            return None
        existente.nombre = grado.nombre
        if hasattr(grado, "descripcion"):
            existente.descripcion = grado.descripcion
        if hasattr(grado, "grado"):
            existente.grado = grado.grado

        # si el repo tiene actualizar, úsalo; si no, commit directo
        if hasattr(GradoRepository, "actualizar"):
            return GradoRepository.actualizar(existente)
        db.session.commit()
        return existente

    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return GradoRepository.borrar_por_id(id)
