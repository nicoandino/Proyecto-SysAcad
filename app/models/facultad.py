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

    # ⚠️ Campo que faltaba y es NOT NULL en DB
    facultad: int = db.Column(db.Integer, nullable=False, default=0)

    nombre: str = db.Column(db.String(100), nullable=False)
    abreviatura: str  = db.Column(db.String(10), nullable=True)
    directorio: str  = db.Column(db.String(100), nullable=True)
    sigla: str  = db.Column(db.String(10), nullable=True)

    # Atributo 'codigo_postal' mapeado a la columna física 'codigopostal'
    codigo_postal: str = db.Column('codigopostal', db.String(10), nullable=True)
    codigo = synonym('codigo_postal')  # alias

    ciudad: str = db.Column(db.String(50), nullable=True)
    domicilio: str = db.Column(db.String(100), nullable=True)
    telefono: str = db.Column(db.String(20), nullable=True)
    contacto: str = db.Column(db.String(100), nullable=True)
    email: str = db.Column(db.String(100), nullable=True)

    universidad_id: int = db.Column(db.Integer, db.ForeignKey('universidades.id'), nullable=True)
    universidad = db.relationship('Universidad', lazy=True)

    autoridades = db.relationship('Autoridad', secondary=facultades_autoridades, back_populates='facultades')

    def asociar_autoridad(self, autoridad):
        if autoridad not in self.autoridades:
            self.autoridades.append(autoridad)

    def desasociar_autoridad(self, autoridad):
        if autoridad in self.autoridades:
            self.autoridades.remove(autoridad)

# Rellenar 'facultad' si llega None (evita NOT NULL)
@event.listens_for(Facultad, "before_insert")
def _fill_facultad_codigo(mapper, connection, target):
    if getattr(target, "facultad", None) is None:
        target.facultad = 0
