from app import db
from app.models import Localidad

class LocalidadRepository:
    @staticmethod
    def crear(localidad: Localidad) -> Localidad:
        db.session.add(localidad)
        db.session.commit()
        return localidad

    @staticmethod
    def buscar_por_id(id: int) -> Localidad:
        return db.session.query(Localidad).filter_by(id=id).first()

    @staticmethod
    def buscar_todos() -> list[Localidad]:
        return db.session.query(Localidad).all()

    @staticmethod
    def actualizar(localidad: Localidad) -> Localidad:
        localidad_existente = db.session.merge(localidad)
        if not localidad_existente:
            return None
        db.session.commit()
        return localidad_existente

    @staticmethod
    def borrar_por_id(id: int) -> bool:
        localidad = db.session.query(Localidad).filter_by(id=id).first()
        if not localidad:
            return False
        db.session.delete(localidad)
        db.session.commit()
        return True
