from app import db
from app.models import Orientacion
from app.repositories import OrientacionRepository

class OrientacionService:
    @staticmethod
    def crear(orientacion: Orientacion) -> Orientacion:
        return OrientacionRepository.crear(orientacion)

    @staticmethod
    def buscar_por_id(id: int) -> Orientacion | None:
        return OrientacionRepository.buscar_por_id(id)
    
    @staticmethod
    def buscar_todos() -> list[Orientacion]:
        return OrientacionRepository.buscar_todos()
    
    @staticmethod
    def actualizar(id: int, datos: Orientacion) -> Orientacion | None:
        existente = OrientacionRepository.buscar_por_id(id)
        if not existente:
            return None
        existente.nombre = datos.nombre
        existente.especialidad_id = datos.especialidad_id
        # importante: tu modelo guarda IDs, no objetos; y las relaciones son viewonly
        existente.plan_id = getattr(datos, "plan_id", None) or getattr(datos, "plan", None) and datos.plan.id
        existente.materia_id = getattr(datos, "materia_id", None) or getattr(datos, "materia", None) and datos.materia.id
        db.session.flush()
        db.session.commit()
        return existente
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return OrientacionRepository.borrar_por_id(id)
