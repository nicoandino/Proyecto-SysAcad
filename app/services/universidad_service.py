from typing import Optional, List
from app.models import Universidad
from app.repositories.universidad_repositorio import UniversidadRepository

class UniversidadService:
    @staticmethod
    def crear(data: Universidad) -> Universidad:
        # data es una instancia de Universidad ya validada
        return UniversidadRepository.crear(data)

    @staticmethod
    def buscar_por_id(id: int) -> Optional[Universidad]:
        return UniversidadRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> List[Universidad]:
        return UniversidadRepository.buscar_todos()

    @staticmethod
    def actualizar(id: int, data: Universidad) -> Optional[Universidad]:
        """
        Actualiza campos básicos de la universidad identificada por id,
        usando el repo.merge() para evitar tener que cargarla primero.
        """
        # Aseguramos que la instancia a mergear tenga el id objetivo
        data.id = id
        u = UniversidadRepository.actualizar_universidad(data)
        return u

    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return UniversidadRepository.borrar_por_id(id) is not None
