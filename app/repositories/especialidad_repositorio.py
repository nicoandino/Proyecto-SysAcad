# app/repositories/especialidad_repository.py
from app import db
from app.models.especialidad import Especialidad

class EspecialidadRepository:

    @staticmethod
    def crear(especialidadd: Especialidad) -> Especialidad:
        db.session.add(especialidadd)
        db.session.flush()
        db.session.commit()
        return especialidadd

    @staticmethod
    def buscar_por_id(id: int) -> Especialidad | None:
        return db.session.query(Especialidad).filter_by(id=id).first()

    @staticmethod
    def buscar_todos() -> list[Especialidad]:
        return db.session.query(Especialidad).all()

    @staticmethod
    def actualizar(especialidad: Especialidad) -> Especialidad | None:
        existente = db.session.merge(especialidad)
        if not existente:
            return None
        db.session.commit()
        return existente

    @staticmethod
    def borrar_por_id(id: int) -> bool:
        obj = db.session.query(Especialidad).filter_by(id=id).first()
        if not obj:
            return False
        db.session.delete(obj)
        db.session.commit()
        return True
