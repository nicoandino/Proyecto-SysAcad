from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class Localidad(db.Model):
    __tablename__ = 'localidades'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.Integer, nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    provincia = db.Column(db.String(50), nullable=True)
    pais = db.Column(db.String(50), nullable=True)
