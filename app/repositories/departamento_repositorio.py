from app import db
from app.models import Departamento

class DepartamentoRepository:

    @staticmethod
    def crear(departamento: Departamento) -> Departamento:
        db.session.add(departamento)
        db.session.flush()   # asigna el id sin cerrar la transacción
        db.session.commit()  # confirma los cambios
        return departamento  # ← devolver la instancia con id

    @staticmethod
    def buscar_por_id(id: int):
        """
        Busca un departamento por su ID.
        :param id: ID del departamento a buscar.
        :return: Objeto Departamento encontrado o None si no se encuentra.
        """
        return db.session.query(Departamento).filter_by(id=id).first()
    
    @staticmethod
    def buscar_todos():
        """
        Busca todos los departamentos en la base de datos.
        :return: Lista de objetos Departamento.
        """
        return db.session.query(Departamento).all()
    
    
    @staticmethod
    def borrar_por_id(id: int) -> Departamento:
        """
        Borra un departamento por su ID.
        :param id: ID del departamento a borrar.
        :return: Objeto Departamento borrado o None si no se encuentra.
        """
        departamento = db.session.query(Departamento).filter_by(id=id).first()
        if not departamento:
            return None
        db.session.delete(departamento)
        db.session.commit()
        return departamento

    @staticmethod
    def guardar(dep: Departamento) -> Departamento:
        db.session.flush()
        db.session.commit()
        return dep

    @staticmethod
    def actualizar(departamento: Departamento) -> Departamento | None:
        existente = db.session.merge(departamento)
        db.session.flush()
        db.session.commit()
        return existente

