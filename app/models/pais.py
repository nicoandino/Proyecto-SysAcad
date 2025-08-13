from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class Pais(db.Model):
    __tablename__ = 'paises'
    # El ID viene del XML; no autoincrementa
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    nombre = db.Column(db.String(100), nullable=False)
