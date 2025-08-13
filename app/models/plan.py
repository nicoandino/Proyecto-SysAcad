# app/models/plan.py
from dataclasses import dataclass
from app import db
from sqlalchemy.orm import relationship

@dataclass(init=False, repr=True, eq=True)
class PlanModel(db.Model):
    __tablename__ = 'planes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'), nullable=False)
    plan = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(100), nullable=True)


