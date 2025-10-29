from dataclasses import dataclass
from app import db
from app.models.materias_especialidades import materias_especialidades

@dataclass(init=False, repr=True, eq=True)
class Especialidad(db.Model):
    __tablename__ = "especialidades"
    __table_args__ = {"extend_existing": True}

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(100), nullable=False)
    letra = db.Column(db.String(1), nullable=True)
    observacion: str = db.Column(db.String(255), nullable=True)

    tipoespecialidad_id: int = db.Column(
        db.Integer,
        db.ForeignKey("tipoespecialidades.id"),
        nullable=True,
    )
    tipoespecialidad = db.relationship("TipoEspecialidad", lazy=True)

    facultad_id: int = db.Column(
        db.Integer,
        db.ForeignKey("facultades.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    facultad = db.relationship("Facultad", back_populates="especialidades")

    # 🔹 N-M con Materias
    materias = db.relationship(
        "Materia",
        secondary=materias_especialidades,
        back_populates="especialidades",
        cascade="all",
    )

    # 🔹 1-N con Planes
    planes = db.relationship(
        "Plan",
        back_populates="especialidad",
        cascade="all, delete-orphan"
    )
    # 🔹 1-N con Alumnos
    alumnos = db.relationship(
        "Alumno",
        back_populates="especialidad",
        cascade="all, delete-orphan"
    )
