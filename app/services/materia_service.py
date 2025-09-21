from app import db
from app.models import Materia
from app.repositories import MateriaRepository, AutoridadRepository

class MateriaService:
    # ===== Métodos con los nombres que usa el test =====
    @staticmethod
    def crear_materia(materia: Materia) -> Materia:
        return MateriaRepository.crear(materia)

    @staticmethod
    def actualizar_materia(id: int, datos: Materia) -> Materia | None:
        existente = MateriaRepository.buscar_por_id(id)
        if not existente:
            return None
        # Actualizamos campos simples
        existente.nombre = datos.nombre
        existente.codigo = datos.codigo
        existente.observacion = datos.observacion
        db.session.flush()
        db.session.commit()
        return existente

    @staticmethod
    def buscar_por_id(id: int) -> Materia | None:
        return MateriaRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[Materia]:
        return MateriaRepository.buscar_todos()

    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return MateriaRepository.borrar_por_id(id) is not None

    # ===== Alias para compatibilidad hacia atrás (si en otro lado usabas crear/actualizar) =====
    @staticmethod
    def crear(materia: Materia) -> Materia:
        return MateriaService.crear_materia(materia)

    @staticmethod
    def actualizar(id: int, datos: Materia) -> Materia | None:
        return MateriaService.actualizar_materia(id, datos)

    # ===== Asociaciones Autoridad <-> Materia (sin cambios) =====
    @staticmethod
    def asociar_autoridad(materia_id: int, autoridad_id: int):
        materia = MateriaRepository.buscar_por_id(materia_id)
        autoridad = AutoridadRepository.buscar_por_id(autoridad_id)
        if not materia or not autoridad:
            raise ValueError("Materia o autoridad no encontrada")
        MateriaRepository.asociar_autoridad(materia, autoridad)

    @staticmethod
    def desasociar_autoridad(materia_id: int, autoridad_id: int):
        materia = MateriaRepository.buscar_por_id(materia_id)
        autoridad = AutoridadRepository.buscar_por_id(autoridad_id)
        if not materia or not autoridad:
            raise ValueError("Materia o autoridad no encontrada")
        MateriaRepository.desasociar_autoridad(materia, autoridad)
