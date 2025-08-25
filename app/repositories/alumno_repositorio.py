# app/repositories/alumno_repositorio.py
from app import db
from app.models.alumno import Alumno

class AlumnoRepository:
    @staticmethod
    def crear(alumno: Alumno) -> None:
        db.session.add(alumno); db.session.commit()

    @staticmethod
    def buscar_por_id(nro_legajo: int) -> Alumno | None:
        # la PK es nro_legajo
        return db.session.get(Alumno, nro_legajo)

    @staticmethod
    def buscar_todos() -> list[Alumno]:
        return db.session.query(Alumno).all()

    @staticmethod
    def actualizar(alumno: Alumno) -> Alumno | None:
        obj = db.session.merge(alumno); db.session.commit(); return obj

    @staticmethod
    def borrar_por_id(nro_legajo: int) -> Alumno | None:
        obj = db.session.get(Alumno, nro_legajo)
        if not obj: return None
        db.session.delete(obj); db.session.commit(); return obj
