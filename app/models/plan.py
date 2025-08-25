from dataclasses import dataclass
from datetime import date
from app import db

@dataclass(init=False, repr=True, eq=True)
class Plan(db.Model):
    __tablename__ = "planes"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=True)
    fecha_fin = db.Column(db.Date, nullable=True)
    observacion = db.Column(db.String(255), nullable=True)

    anio = db.Column(db.Integer, nullable=True)

    especialidad_id = db.Column('especialidad', db.Integer, nullable=True)

    especialidad = db.relationship(
        'Especialidad',
        primaryjoin="foreign(Plan.especialidad_id)==Especialidad.id",
        lazy=True,
        viewonly=True,
    )


