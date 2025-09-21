from app import db
from app.models import Orientacion

class OrientacionRepository:
    @staticmethod
    def crear(orientacion: Orientacion) -> Orientacion:
        db.session.add(orientacion)
        db.session.flush()
        db.session.refresh(orientacion)
        db.session.commit()
        return orientacion

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(Orientacion).filter_by(id=id).first()
    
    @staticmethod
    def buscar_todos():
        return db.session.query(Orientacion).all()
    
    @staticmethod
    def actualizar(orientacion: Orientacion) -> Orientacion | None:
        merged = db.session.merge(orientacion)
        db.session.flush()
        db.session.commit()
        return merged
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        orientacion = db.session.query(Orientacion).filter_by(id=id).first()
        if not orientacion:
            return False
        db.session.delete(orientacion)
        db.session.commit()
        return True
