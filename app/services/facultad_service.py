from app.models import Facultad
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
        # Campo obligatorio: algunos modelos usan 'facultad', otros 'nombre'
        if hasattr(facultad, "facultad"):
            facultad.facultad = FacultadService._texto_obligatorio(facultad.facultad, "facultad")
        elif hasattr(facultad, "nombre"):
            facultad.nombre = FacultadService._texto_obligatorio(facultad.nombre, "nombre")

        # Normalización de strings comunes (si existen en el modelo)
        for attr in [
            "abreviatura", "directorio", "sigla", "codigo_postal",
            "ciudad", "domicilio", "telefono", "contacto"
        ]:
            if hasattr(facultad, attr):
                setattr(facultad, attr, FacultadService._normalizar_str(getattr(facultad, attr)))

        return FacultadRepository.crear(facultad)

    @staticmethod
    def buscar_por_id(id: int) -> Facultad:
        return FacultadRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[Facultad]:
        return FacultadRepository.buscar_todos()

    @staticmethod
    def actualizar_facultad(id: int, facultad: Facultad) -> Facultad:
        existente = FacultadRepository.buscar_por_id(id)
        if not existente:
            return None

        # Actualiza y normaliza solo los atributos presentes
        campos = [
            "facultad", "nombre", "abreviatura", "directorio", "sigla",
            "codigo_postal", "ciudad", "domicilio", "telefono", "contacto"
        ]
        for attr in campos:
            if hasattr(existente, attr) and hasattr(facultad, attr):
                valor = getattr(facultad, attr)
                if attr in ("facultad", "nombre"):
                    valor = FacultadService._texto_obligatorio(valor, attr)
                else:
                    valor = FacultadService._normalizar_str(valor)
                setattr(existente, attr, valor)

        # Si tu repositorio tiene un método de actualización, úsalo:
        if hasattr(FacultadRepository, "actualizar_facultad"):
            return FacultadRepository.actualizar_facultad(existente)

        # Si no, al menos devolvemos el objeto modificado (asumiendo flush/commit fuera)
        return existente

    @staticmethod
    def borrar_por_id(id: int) -> Facultad:
        fac = FacultadRepository.buscar_por_id(id)
        if not fac:
            return None
        if hasattr(FacultadRepository, "borrar_por_id"):
            return FacultadRepository.borrar_por_id(id)
        return fac

    
        