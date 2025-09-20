# app/repositories/grado_repository.py
from app import db
from app.models import Grado

class GradoRepository:
    @staticmethod
    def crear(grado: Grado) -> Grado:
        db.session.add(grado)
        db.session.flush()   # asegura que grado.id quede asignado
        db.session.commit()
        return grado

    @staticmethod
    def buscar_por_id(id: int) -> Grado | None:
        return db.session.query(Grado).filter_by(id=id).first()

    @staticmethod
    def buscar_todos() -> list[Grado]:
        return db.session.query(Grado).all()

    @staticmethod
    def actualizar_grado(grado: Grado) -> Grado | None:
        existente = db.session.merge(grado)
        if not existente:
            return None
        db.session.commit()   # persistir cambios
        return existente

    # alias opcional para que el service pueda llamarlo como "actualizar"
    @staticmethod
    def actualizar(grado: Grado) -> Grado | None:
        return GradoRepository.actualizar_grado(grado)

    @staticmethod
    def borrar_por_id(id: int) -> bool:
        obj = db.session.query(Grado).filter_by(id=id).first()
        if not obj:
            return False
        db.session.delete(obj)
        db.session.commit()
        return True
