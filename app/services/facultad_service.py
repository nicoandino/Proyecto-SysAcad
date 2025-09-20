# app/services/facultad_service.py
from app import db
from app.models import Facultad, Autoridad
from app.repositories.facultad_repositorio import FacultadRepository

class FacultadService:
    @staticmethod
    def _texto_obligatorio(valor, nombre_campo):
        if valor is None:
            raise ValueError(f"{nombre_campo} es obligatorio")
        valor = str(valor).strip()
        if not valor:
            raise ValueError(f"{nombre_campo} no puede estar vacío")
        return valor

    @staticmethod
    def _normalizar_str(v):
        if v is None:
            return None
        return str(v).strip()

    @staticmethod
    def crear_facultad(facultad: Facultad):
        if hasattr(facultad, "facultad"):
            facultad.facultad = FacultadService._texto_obligatorio(facultad.facultad, "facultad")
        elif hasattr(facultad, "nombre"):
            facultad.nombre = FacultadService._texto_obligatorio(facultad.nombre, "nombre")

        for attr in ["abreviatura","directorio","sigla","codigo_postal","ciudad","domicilio","telefono","contacto"]:
            if hasattr(facultad, attr):
                setattr(facultad, attr, FacultadService._normalizar_str(getattr(facultad, attr)))

        return FacultadRepository.crear(facultad)

    @staticmethod
    def buscar_por_id(id: int) -> Facultad | None:
        return FacultadRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[Facultad]:
        return FacultadRepository.buscar_todos()

    # ===== métodos esperados por el test =====
    @staticmethod
    def actualizar(id: int, facultad: Facultad) -> Facultad | None:
        return FacultadService.actualizar_facultad(id, facultad)

    @staticmethod
    def actualizar_facultad(id: int, facultad: Facultad) -> Facultad | None:
        existente = FacultadRepository.buscar_por_id(id)
        if not existente:
            return None

        campos = ["facultad","nombre","abreviatura","directorio","sigla","codigo_postal","ciudad","domicilio","telefono","contacto","email"]
        for attr in campos:
            if hasattr(facultad, attr):
                valor = getattr(facultad, attr)
                if attr in ("facultad","nombre"):
                    valor = FacultadService._texto_obligatorio(valor, attr)
                else:
                    valor = FacultadService._normalizar_str(valor)
                setattr(existente, attr, valor)

        # persistir usando el repo (hace commit adentro)
        if hasattr(FacultadRepository, "actualizar_facultad"):
            return FacultadRepository.actualizar_facultad(existente)
        db.session.commit()
        return existente

    @staticmethod
    def borrar_por_id(id: int) -> bool:
        existente = FacultadRepository.buscar_por_id(id)
        if not existente:
            return False
        borrado = FacultadRepository.borrar_por_id(id)   # repo devuelve instancia o None
        return borrado is not None

    @staticmethod
    def asociar_autoridad(facultad_id: int, autoridad_id: int) -> bool:
        fac = FacultadRepository.buscar_por_id(facultad_id)
        if not fac:
            return False
        aut = db.session.get(Autoridad, autoridad_id)
        if not aut:
            return False
        if aut not in fac.autoridades:
            fac.autoridades.append(aut)
            db.session.commit()
        return True

    @staticmethod
    def desasociar_autoridad(facultad_id: int, autoridad_id: int) -> bool:
        fac = FacultadRepository.buscar_por_id(facultad_id)
        if not fac:
            return False
        aut = db.session.get(Autoridad, autoridad_id)
        if not aut:
            return False
        if aut in fac.autoridades:
            fac.autoridades.remove(aut)
            db.session.commit()
        return True
