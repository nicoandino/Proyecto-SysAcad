from dataclasses import dataclass
from app import db
from sqlalchemy import event

@dataclass(init=False, repr=True, eq=True)
class Cargo(db.Model):
    __tablename__ = 'cargos'
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)

    descripcion = db.Column(
        db.String(255),
        nullable=False,
        default="Sin descripción",
        server_default="Sin descripción",
    )

    grado = db.Column(db.Integer, nullable=True)


    categoria_cargo_id = db.Column(db.Integer, db.ForeignKey('categoriacargos.id'), nullable=True)
    categoria_cargo = db.relationship('CategoriaCargo', lazy=True)

    tipo_dedicacion_id = db.Column(db.Integer, db.ForeignKey('tipodedicaciones.id'), nullable=True)
    tipo_dedicacion = db.relationship('TipoDedicacion', lazy=True)

    def __init__(self, **kwargs):
        desc = (kwargs.pop("descripcion", None) or "").strip()
        if not desc:
            desc = "Sin descripción"
        super().__init__(descripcion=desc, **kwargs)

@event.listens_for(Cargo, "before_insert")
def _cargo_before_insert(mapper, connection, target):
    desc = (target.descripcion or "").strip()
    if not desc:
        target.descripcion = "Sin descripción"

@event.listens_for(Cargo, "before_update")
def _cargo_before_update(mapper, connection, target):
    desc = (target.descripcion or "").strip()
    if not desc:
        target.descripcion = "Sin descripción"



