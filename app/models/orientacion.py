from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class Orientacion(db.Model):
    __tablename__ = "orientaciones"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)

    # IDs "sueltos" (sin FK dura) mapeados a las columnas reales
    especialidad_id = db.Column('especialidad', db.Integer, nullable=True)
    plan_id = db.Column('plan', db.Integer, nullable=True)
    materia_id = db.Column('materia', db.Integer, nullable=True)

    # Relaciones solo de lectura (no imponen constraint en INSERT)
    especialidad = db.relationship(
        'Especialidad',
        primaryjoin="foreign(Orientacion.especialidad_id)==Especialidad.id",
        lazy=True,
        viewonly=True,
    )
    plan = db.relationship(
        'Plan',
        primaryjoin="foreign(Orientacion.plan_id)==Plan.id",
        lazy=True,
        viewonly=True,
    )
    materia = db.relationship(
        'Materia',
        primaryjoin="foreign(Orientacion.materia_id)==Materia.id",
        lazy=True,
        viewonly=True,
    )




    