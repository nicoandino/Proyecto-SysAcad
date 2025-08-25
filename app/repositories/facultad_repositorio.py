from app import db
from app.models import Facultad

class FacultadRepository:
    @staticmethod
    def crear(facultad: Facultad) -> Facultad:
        # Validaciones obligatorias
        if not hasattr(facultad, "facultad") or facultad.facultad is None or str(facultad.facultad).strip() == "":
            raise ValueError("facultad es obligatoria")
        # nombre también obligatorio según tu XML/uso
        if not hasattr(facultad, "nombre") or facultad.nombre is None or not str(facultad.nombre).strip():
            raise ValueError("nombre es obligatorio")

        # Normalización mínima
        facultad.nombre = str(facultad.nombre).strip()

        db.session.add(facultad)
        db.session.commit()
        return facultad

    @staticmethod
    def buscar_por_id(id: int) -> Facultad:
        return db.session.query(Facultad).filter_by(id=id).first()

    @staticmethod
    def buscar_todos() -> list[Facultad]:
        return db.session.query(Facultad).all()

    @staticmethod
    def actualizar_facultad(facultad: Facultad) -> Facultad:
        # Aseguramos campos obligatorios antes de persistir
        if not hasattr(facultad, "facultad") or facultad.facultad is None or str(facultad.facultad).strip() == "":
            raise ValueError("facultad es obligatoria")
        if not hasattr(facultad, "nombre") or facultad.nombre is None or not str(facultad.nombre).strip():
            raise ValueError("nombre es obligatorio")

        facultad.nombre = str(facultad.nombre).strip()

        facultad_existente = db.session.merge(facultad)
        db.session.commit()
        return facultad_existente

    @staticmethod
    def borrar_por_id(id: int) -> Facultad:
        fac = db.session.query(Facultad).filter_by(id=id).first()
        if not fac:
            return None
        db.session.delete(fac)
        db.session.commit()
        return fac

