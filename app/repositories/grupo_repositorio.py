# app/repositories/grupo_repository.py
from app import db
from app.models import Grupo

class GrupoRepository:
    @staticmethod
    def crear(grupo: Grupo) -> Grupo:
        db.session.add(grupo)
        db.session.flush()      # asegura que grupo.id se asigne
        db.session.commit()
        return grupo            # <- devolver instancia

    @staticmethod
    def buscar_por_id(id: int) -> Grupo | None:
        return db.session.query(Grupo).filter_by(id=id).first()
    
    @staticmethod
    def buscar_todos() -> list[Grupo]:
        return db.session.query(Grupo).all()
    
    @staticmethod
    def actualizar(grupo: Grupo) -> Grupo | None:
        existente = db.session.merge(grupo)
        if not existente:
            return None
        db.session.commit()     # <- persistir cambios
        return existente
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        grupo = db.session.query(Grupo).filter_by(id=id).first()
        if not grupo:
            return False
        db.session.delete(grupo)
        db.session.commit()
        return True
