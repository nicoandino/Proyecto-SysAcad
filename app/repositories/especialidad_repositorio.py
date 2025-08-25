from app import db
from app.models import especialidad

class EspecialidadRepository:

    @staticmethod
    def crear(especialidadd):
        db.session.add(especialidadd)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(especialidad).filter_by(id=id).first()

    @staticmethod
    def buscar_todos():
        return db.session.query(especialidad).all()

    @staticmethod
    def actualizar(especialidad) -> especialidad:
        especialidad_existente = db.session.merge(especialidad)
        if not especialidad_existente:
            return None
        return especialidad_existente
    
    @staticmethod
    def borrar_por_id(id: int) -> especialidad:
        especialidad = db.session.query(especialidad).filter_by(id=id).first()
        if not especialidad:
            return None
        db.session.delete(especialidad)
        db.session.commit()
        return especialidad

