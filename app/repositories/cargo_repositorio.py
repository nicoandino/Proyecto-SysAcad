from app import db
from app.models.autoridad import Cargo

class CargoRepository:
    @staticmethod
    def crear(cargo: Cargo) -> Cargo:
        desc = getattr(cargo, "descripcion", None)
        if (desc is None or not str(desc).strip()) and hasattr(cargo, "nombre"):
            desc = getattr(cargo, "nombre")
        if desc is None or not str(desc).strip():
            raise ValueError("descripcion es obligatoria")
        cargo.descripcion = str(desc).strip()
        db.session.add(cargo)
        db.session.commit()
        return cargo

    @staticmethod
    def buscar_por_id(id: int) -> Cargo:
        return db.session.query(Cargo).filter_by(idCargo=id).first()

    @staticmethod
    def buscar_todos() -> list[Cargo]:
        return db.session.query(Cargo).all()

    @staticmethod
    def actualizar_cargo(cargo: Cargo) -> Cargo:
        desc = getattr(cargo, "descripcion", None)
        if (desc is None or not str(desc).strip()) and hasattr(cargo, "nombre"):
            desc = getattr(cargo, "nombre")
        if desc is None or not str(desc).strip():
            raise ValueError("descripcion es obligatoria")
        cargo.descripcion = str(desc).strip()
        cargo_existente = db.session.merge(cargo)
        db.session.commit()
        return cargo_existente

    @staticmethod
    def borrar_por_id(id: int) -> Cargo:
        cargo = db.session.query(Cargo).filter_by(idCargo=id).first()
        if not cargo:
            return None
        db.session.delete(cargo)
        db.session.commit()
        return cargo
