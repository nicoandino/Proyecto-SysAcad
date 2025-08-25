from app import db
from app.models import Materia

class MateriaRepository:
    """
    Clase de repositorio para la entidad Materia.
    """
    @staticmethod
    def crear(materia):
        db.session.add(materia)
        db.session.commit()
    
    @staticmethod    
    def buscar_por_id(id: int):
        return db.session.query(Materia).filter_by(id=id).first()
    
    @staticmethod
    def buscar_todos():
        return db.session.query(Materia).all()
    
    @staticmethod
    def actualizar_materia(materia) -> Materia:
        materia_existente = db.session.merge(materia)
        if not materia_existente:
            return None
        return materia_existente
    
    @staticmethod
    def borrar_por_id(id: int) -> Materia:
        materia = db.session.query(Materia).filter_by(id=id).first()
        if not materia:
            return None
        db.session.delete(materia)
        db.session.commit()
        return materia