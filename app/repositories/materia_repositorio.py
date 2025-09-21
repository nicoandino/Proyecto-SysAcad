from app import db
from app.models import Materia

class MateriaRepository:
    @staticmethod
    def crear(materia: Materia) -> Materia:
        db.session.add(materia)
        db.session.flush()          # asegura materia.id disponible
        db.session.refresh(materia) # opcional: sincroniza estado
        db.session.commit()
        return materia
    
    @staticmethod    
    def buscar_por_id(id: int) -> Materia | None:
        return db.session.query(Materia).filter_by(id=id).first()
    
    @staticmethod
    def buscar_todos() -> list[Materia]:
        return db.session.query(Materia).all()
    
    @staticmethod
    def actualizar_materia(materia: Materia) -> Materia | None:
        # Si en algún lugar lo usás, al menos que haga commit y devuelva.
        merged = db.session.merge(materia)
        db.session.flush()
        db.session.commit()
        return merged
    
    @staticmethod
    def borrar_por_id(id: int) -> Materia | None:
        materia = db.session.query(Materia).filter_by(id=id).first()
        if not materia:
            return None
        db.session.delete(materia)
        db.session.commit()
        return materia

    # Si usás asociar/desasociar en el service, podrías tener:
    @staticmethod
    def asociar_autoridad(materia: Materia, autoridad) -> Materia:
        materia.asociar_autoridad(autoridad)
        db.session.flush()
        db.session.commit()
        return materia

    @staticmethod
    def desasociar_autoridad(materia: Materia, autoridad) -> Materia:
        materia.desasociar_autoridad(autoridad)
        db.session.flush()
        db.session.commit()
        return materia
