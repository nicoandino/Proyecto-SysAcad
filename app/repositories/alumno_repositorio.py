# app/repositories/alumno_repositorio.py
from app import db
from app.models.alumnos import Alumnos

class AlumnoRepository:
    @staticmethod
    def crear(alumno: Alumnos) -> None:
        db.session.add(alumno); db.session.commit()

    @staticmethod
    def buscar_por_id(nro_legajo: int) -> Alumnos | None:  # 'id' = legajo
        return db.session.get(Alumnos, nro_legajo)

    @staticmethod
    def buscar_todos() -> list[Alumnos]:
        return db.session.query(Alumnos).all()

    @staticmethod
    def actualizar(alumno: Alumnos) -> Alumnos | None:
        obj = db.session.merge(alumno); db.session.commit(); return obj

    @staticmethod
    def borrar_por_id(nro_legajo: int) -> Alumnos | None:
        obj = db.session.get(Alumnos, nro_legajo)
        if not obj: return None
        db.session.delete(obj); db.session.commit(); return obj
