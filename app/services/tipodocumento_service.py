from app.models import TipoDocumento
from app.repositories import TipoDocumentoRepository
from app import db

class TipoDocumentoService:

    @staticmethod
    def crear(tipodocumento: TipoDocumento):
        return TipoDocumentoRepository.crear(tipodocumento)

    @staticmethod
    def buscar_por_id(id: int) -> TipoDocumento:
        return TipoDocumentoRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[TipoDocumento]:
        return TipoDocumentoRepository.buscar_todos()

    @staticmethod
    def actualizar(id: int, tipodocumento: TipoDocumento) -> TipoDocumento:
        tipodocumento_existente = TipoDocumentoRepository.buscar_por_id(id)
        if not tipodocumento_existente:
            return None

        # 🔹 Campos actualizados según tu modelo
        tipodocumento_existente.sigla = tipodocumento.sigla
        tipodocumento_existente.nombre = tipodocumento.nombre
        tipodocumento_existente.descripcion = tipodocumento.descripcion

        db.session.commit()
        return tipodocumento_existente

    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return TipoDocumentoRepository.borrar_por_id(id)
