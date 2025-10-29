from dataclasses import dataclass
from datetime import date
from app import db
from app.models.planes_materias import planes_materias  # 🔹 importa la tabla intermedia

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

    # 🔹 Relación 1–N: cada Plan pertenece a una sola Especialidad
    especialidad_id = db.Column(
        db.Integer,
        db.ForeignKey("especialidades.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    especialidad = db.relationship(
        "Especialidad",
        back_populates="planes"
    )

    # 🔹 Relación N–M: cada Plan puede incluir muchas Materias
    materias = db.relationship(
        "Materia",
        secondary=planes_materias,
        back_populates="planes",
        cascade="all"
    )
