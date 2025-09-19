# app/services/departamento_service.py
from app.models import Departamento
from app.repositories import DepartamentoRepository

class DepartamentoService:
    @staticmethod
    def crear(departamento: Departamento) -> Departamento:
        # IMPORTANTE: devolver la entidad ya persistida
        return DepartamentoRepository.crear(departamento)

    @staticmethod
    def buscar_por_id(id: int) -> Departamento | None:
        return DepartamentoRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[Departamento]:
        return DepartamentoRepository.buscar_todos()

    @staticmethod
    def actualizar(id: int, datos: Departamento) -> Departamento | None:
        existente = DepartamentoRepository.buscar_por_id(id)
        if not existente:
            return None
        existente.nombre = datos.nombre
        # opcional: que el repo flushee/commitee cambios
        return DepartamentoRepository.guardar(existente)

    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return DepartamentoRepository.borrar_por_id(id)

