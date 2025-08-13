from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class OrientacionModel(db.Model):
    __tablename__ = 'orientaciones'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    especialidad_id = db.Column(db.Integer, nullable=False)  # Eliminada FK para evitar dependencia
    plan = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(150), nullable=True)

    # No se declara relationship para evitar dependencia circular con EspecialidadModel
