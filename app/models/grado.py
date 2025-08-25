from dataclasses import dataclass
from app import db
from sqlalchemy import event

@dataclass(init=False, repr=True, eq=True)
class Grado(db.Model):
    __tablename__ = 'grados'
    __table_args__ = {"extend_existing": True}

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grado: int = db.Column(db.Integer, nullable=False)         
    nombre: str = db.Column(db.String(50), nullable=False)
    descripcion: str = db.Column(db.String(200), nullable=False)

@event.listens_for(Grado, "before_insert")
def _fill_grado_descripcion(mapper, connection, target):
    desc = getattr(target, "descripcion", None)
    if desc is None or not str(desc).strip():
        target.descripcion = (getattr(target, "nombre", "") or "").strip()

GradoModel = Grado



    