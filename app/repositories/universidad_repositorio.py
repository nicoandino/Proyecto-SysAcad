# app/repositories/universidad_repository.py
from app import db
from app.models import Universidad

class UniversidadRepository:
    @staticmethod
    def crear(universidad: Universidad) -> Universidad:
        db.session.add(universidad)
        db.session.flush()
        db.session.refresh(universidad)
        db.session.commit()
        return universidad

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(Universidad).filter_by(id=id).first()

    @staticmethod
    def buscar_todos():
        return db.session.query(Universidad).all()
    
    @staticmethod
    def actualizar_universidad(universidad: Universidad) -> Universidad | None:
        merged = db.session.merge(universidad)
        db.session.flush()
        db.session.commit()
        return merged
    
    @staticmethod
    def borrar_por_id(id: int) -> Universidad | None:
        universidad = db.session.query(Universidad).filter_by(id=id).first()
        if not universidad:
            return None
        db.session.delete(universidad)
        db.session.commit()
        return universidad
