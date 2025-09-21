from dataclasses import dataclass 
from app import db

@dataclass(init=False, repr=True, eq=True)
class TipoEspecialidad(db.Model):
    __tablename__ = 'tipoespecialidades'
    __table_args__ = {"extend_existing": True}

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)       
    nombre: str = db.Column(db.String(100), nullable=False)
    # ✅ requerido por los tests
    nivel: str = db.Column(db.String(50), nullable=False, default="Avanzado")
