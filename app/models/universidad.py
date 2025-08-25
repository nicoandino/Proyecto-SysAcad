# app/models/universidad.py
from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class Universidad(db.Model):
    __tablename__ = "universidades"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    sigla = db.Column(db.String(50), nullable=True)  

