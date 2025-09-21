# app/services/universidad_service.py
from typing import Optional, List
from app.models import Universidad
from app.repositories.universidad_repositorio import UniversidadRepository  # ojo al nombre del módulo

class UniversidadService:
    @staticmethod
    def crear(data: Universidad) -> Universidad:
        return UniversidadRepository.crear(data)

    @staticmethod
    def buscar_por_id(id: int) -> Optional[Universidad]:
        return UniversidadRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> List[Universidad]:
        return UniversidadRepository.buscar_todos()

    @staticmethod
    def actualizar(id: int, data: Universidad) -> Optional[Universidad]:
        data.id = id
        return UniversidadRepository.actualizar_universidad(data)

    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return UniversidadRepository.borrar_por_id(id) is not None
