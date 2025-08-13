from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class EspecialidadModel(db.Model):
    __tablename__ = 'especialidades'
    __table_args__ = (
        db.UniqueConstraint('especialidad', name='uq_especialidades_especialidad'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    especialidad = db.Column(db.Integer, nullable=False, index=True)
    nombre = db.Column(db.String(100), nullable=False)
    letra = db.Column(db.String(1), nullable=True)
    observacion = db.Column(db.String(255), nullable=True)

    # Campos para referencias, sin relationships para evitar dependencias circulares
    # orientacion_id = db.Column(db.Integer, db.ForeignKey('orientaciones.id'))
    # plan_id = db.Column(db.Integer, db.ForeignKey('planes.id'))
