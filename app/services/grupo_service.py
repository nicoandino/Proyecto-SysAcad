# app/services/grupo_service.py
from app.models import Grupo
from app.repositories.grupo_repositorio import GrupoRepository  # <- import explícito

class GrupoService:
    @staticmethod
    def crear(grupo: Grupo) -> Grupo:
        return GrupoRepository.crear(grupo)  # <- devolver

    @staticmethod
    def buscar_por_id(id: int) -> Grupo | None:
        return GrupoRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[Grupo]:
        return GrupoRepository.buscar_todos()
    
    @staticmethod
    def actualizar(id: int, grupo: Grupo) -> Grupo | None:
        existente = GrupoRepository.buscar_por_id(id)
        if not existente:
            return None
        existente.nombre = grupo.nombre
        return GrupoRepository.actualizar(existente)  # hace commit

    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return GrupoRepository.borrar_por_id(id)
