from dataclasses import dataclass
from app.models.materias_especialidades import materias_especialidades
from app.models.relations import autoridades_materias
from app import db

@dataclass(init=False, repr=True, eq=True)
class Materia(db.Model):
    __tablename__ = "materias"
    __table_args__ = {"extend_existing": True}

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(255), nullable=False)
    codigo: str = db.Column(db.String(20), nullable=True)
    observacion: str = db.Column(db.String(255), nullable=True)

    # 🔹 Relación N-M con Especialidad
    especialidades = db.relationship(
        "Especialidad",
        secondary=materias_especialidades,
        back_populates="materias",
        cascade="all",
    )

    # 🔹 Relación N-M con Autoridad
    autoridades = db.relationship(
        "Autoridad",
        secondary=autoridades_materias,
        back_populates="materias",
    )

    # 🔹 Relación N-M con Planes
    planes = db.relationship(
        "Plan",
        secondary="planes_materias",
        back_populates="materias"
    )

    def asociar_autoridad(self, autoridad):
        if autoridad not in self.autoridades:
            self.autoridades.append(autoridad)

    def desasociar_autoridad(self, autoridad):
        if autoridad in self.autoridades:
            self.autoridades.remove(autoridad)
