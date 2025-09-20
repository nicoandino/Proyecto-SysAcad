from app.models import Especialidad
from app.repositories.especialidad_repositorio import EspecialidadRepository
from app import db

@staticmethod
def actualizar(id: int, especialidad: Especialidad) -> Especialidad:
    especialidad_existente = EspecialidadRepository.buscar_por_id(id)
    if not especialidad_existente:
        return None
    especialidad_existente.nombre = especialidad.nombre
    especialidad_existente.letra = especialidad.letra
    especialidad_existente.observacion = especialidad.observacion
    especialidad_existente.tipoespecialidad = especialidad.tipoespecialidad
    especialidad_existente.facultad = especialidad.facultad
    db.session.commit()   # <- acá
    return especialidad_existente

class EspecialidadService:

    @staticmethod
    def crear(especialidad):
        return EspecialidadRepository.crear(especialidad)

    @staticmethod
    def buscar_por_id(id: int) -> Especialidad:
        # pyrefly: ignore  # bad-return
        return EspecialidadRepository.buscar_por_id(id)
    
    @staticmethod
    def buscar_todos() -> list[Especialidad]:
        return EspecialidadRepository.buscar_todos()

    @staticmethod
    def actualizar(id: int, especialidad: Especialidad) -> Especialidad:
        especialidad_existente = EspecialidadRepository.buscar_por_id(id)
        if not especialidad_existente:
            return None
        especialidad_existente.nombre = especialidad.nombre
        especialidad_existente.letra = especialidad.letra
        especialidad_existente.observacion = especialidad.observacion
        especialidad_existente.tipoespecialidad = especialidad.tipoespecialidad
        especialidad_existente.facultad = especialidad.facultad
        db.session.commit()   # <- acá
        return especialidad_existente
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return EspecialidadRepository.borrar_por_id(id)
