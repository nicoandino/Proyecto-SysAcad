from app import db
from app.models import Plan
from app.repositories import PlanRepository

class PlanService:
    @staticmethod
    def crear(plan: Plan) -> Plan:
        return PlanRepository.crear(plan)
    
    @staticmethod
    def buscar_por_id(id: int) -> Plan | None:
        return PlanRepository.buscar_por_id(id)
    
    @staticmethod
    def buscar_todos() -> list[Plan]:
        return PlanRepository.buscar_todos()
    
    @staticmethod
    def actualizar(id: int, datos: Plan) -> Plan | None:
        existente = PlanRepository.buscar_por_id(id)
        if not existente:
            return None
        # Actualizar campos que usa el test
        existente.nombre = datos.nombre
        existente.fecha_inicio = datos.fecha_inicio
        existente.fecha_fin = datos.fecha_fin
        existente.observacion = datos.observacion
        db.session.flush()
        db.session.commit()
        return existente
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return PlanRepository.borrar_por_id(id)
