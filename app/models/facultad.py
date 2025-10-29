# app/models/facultad.py
from dataclasses import dataclass
from sqlalchemy.orm import synonym
from sqlalchemy import event
from app import db
from app.models.relations import facultades_autoridades

@dataclass(init=False, repr=True, eq=True)
class Facultad(db.Model):
    __tablename__ = 'facultades'
    __table_args__ = {"extend_existing": True}
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    facultad: int = db.Column(db.Integer, nullable=False, default=0)
    nombre: str = db.Column(db.String(100), nullable=False)
    abreviatura: str  = db.Column(db.String(10), nullable=True)
    directorio: str  = db.Column(db.String(100), nullable=True)
    sigla: str  = db.Column(db.String(10), nullable=True)
    codigo_postal: str = db.Column('codigopostal', db.String(10), nullable=True)
    codigo = synonym('codigo_postal')
    ciudad: str = db.Column(db.String(50), nullable=True)
    domicilio: str = db.Column(db.String(100), nullable=True)
    telefono: str = db.Column(db.String(20), nullable=True)
    contacto: str = db.Column(db.String(100), nullable=True)
    email: str = db.Column(db.String(100), nullable=True)

    
    universidad_id: int = db.Column(db.Integer,db.ForeignKey('universidades.id', ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    universidad = db.relationship('Universidad', back_populates='facultades')
    
    # Facultades -> Especialidades (1—N)
    especialidades = db.relationship(
        "Especialidad",
        back_populates="facultad",
        cascade="all, delete-orphan"
    )
    autoridades = db.relationship('Autoridad', secondary=facultades_autoridades, back_populates='facultades')

    #relacion alumnos
    alumnos = db.relationship("Alumno",back_populates="facultad",cascade="all, delete-orphan")
    









    def asociar_autoridad(self, autoridad):
        if autoridad not in self.autoridades:
            self.autoridades.append(autoridad)

    def desasociar_autoridad(self, autoridad):
        if autoridad in self.autoridades:
            self.autoridades.remove(autoridad)

@event.listens_for(Facultad, "before_insert")
def _fill_facultad_codigo(mapper, connection, target):
    if getattr(target, "facultad", None) is None:
        target.facultad = 0
