from app import db
from app.models import Plan

class PlanRepository:
    @staticmethod
    def crear(plan: Plan) -> Plan:
        db.session.add(plan)
        db.session.flush()
        db.session.refresh(plan)
        db.session.commit()
        return plan

    @staticmethod
    def buscar_por_id(id: int) -> Plan | None:
        return db.session.query(Plan).filter_by(id=id).first()
    
    @staticmethod
    def buscar_todos() -> list[Plan]:
        return db.session.query(Plan).all()
    
    @staticmethod
    def actualizar(plan: Plan) -> Plan | None:
        merged = db.session.merge(plan)
        db.session.flush()
        db.session.commit()
        return merged
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        plan = db.session.query(Plan).filter_by(id=id).first()
        if not plan:
            return False
        db.session.delete(plan)
        db.session.commit()
        return True
