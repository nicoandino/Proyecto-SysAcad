from dataclasses import dataclass
from app import db
from app.models import TipoEspecialidad

@dataclass(init=False, repr=True, eq=True)
class Especialidad(db.Model):
    __tablename__ = 'especialidades'
    __table_args__ = {"extend_existing": True}

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(100), nullable=False)
    letra = db.Column(db.String(1), nullable=True)
    observacion: str = db.Column(db.String(255), nullable=True)

    tipoespecialidad_id: int = db.Column(
        db.Integer,
        db.ForeignKey('tipoespecialidades.id'),
        nullable=True   # <--- ahora acepta NULL
    )
    tipoespecialidad = db.relationship('TipoEspecialidad', lazy=True)

    facultad_id: int = db.Column(
        db.Integer,
        db.ForeignKey('facultades.id'),
        nullable=True   # <--- ahora acepta NULL
    )
    facultad = db.relationship('Facultad', lazy=True)
