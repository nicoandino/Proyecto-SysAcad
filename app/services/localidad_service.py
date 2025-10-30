from app.models import Localidad
from app.repositories import LocalidadRepository

class LocalidadService:
    @staticmethod
    def crear(localidad: Localidad) -> Localidad:
        return LocalidadRepository.crear(localidad)

    @staticmethod
    def buscar_por_id(id: int) -> Localidad:
        return LocalidadRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[Localidad]:
        return LocalidadRepository.buscar_todos()

    @staticmethod
    def actualizar(id: int, localidad: Localidad) -> Localidad:
        localidad_existente = LocalidadRepository.buscar_por_id(id)
        if not localidad_existente:
            return None
        localidad_existente.codigo = localidad.codigo
        localidad_existente.ciudad = localidad.ciudad
        localidad_existente.provincia = localidad.provincia
        localidad_existente.pais = localidad.pais
        return localidad_existente

    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return LocalidadRepository.borrar_por_id(id)
