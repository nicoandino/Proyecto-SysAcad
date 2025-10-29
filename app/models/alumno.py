# app/models/alumno.py
from dataclasses import dataclass
from datetime import date
from app import db

@dataclass(init=False, repr=True, eq=True)
class Alumno(db.Model):
    __tablename__ = "alumnos"
    __table_args__ = {"extend_existing": True}
    apellido         = db.Column(db.String(255), nullable=False)
    nombre           = db.Column(db.String(255), nullable=False)
    nro_documento    = db.Column(db.Integer, nullable=False)
    tipo_documento   = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    sexo             = db.Column(db.String(1), nullable=False)
    nro_legajo       = db.Column(db.Integer, primary_key=True)
    fecha_ingreso    = db.Column(db.Date, nullable=False)
    
    #relacione facultad
    facultad_id = db.Column(db.Integer, db.ForeignKey('facultades.id', ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    facultad = db.relationship("Facultad", back_populates="alumnos")

    #relacion especialidad
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidades.id', ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    especialidad = db.relationship("Especialidad", back_populates="alumnos")

    #relacion tipo documento
    tipo_documento_id = db.Column(db.Integer, db.ForeignKey('tipodocumentos.id', ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    tipo_documento = db.relationship("TipoDocumento", back_populates="alumnos")

    #relacion pais
    pais_id = db.Column(db.Integer, db.ForeignKey('paises.id', ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    pais = db.relationship("Pais")
    
    @property
    def nrodocumento(self):
        return self.nro_documento
    # ---- Alias/compatibilidad ----
    @property
    def id(self) -> int:
        """Alias para código que aún espera `alumno.id`."""
        return self.nro_legajo

    @property
    def nrodocumento(self) -> str:
        """Alias sin guion bajo para código viejo."""
        return self.nro_documento

# Alias de clase para imports antiguos (si en algún lado usan `Alumnos`)
Alumnos = Alumno
