from app.models.autoridad import Cargo
from app.repositories.cargo_repositorio import CargoRepository

class CargoService:
    @staticmethod
    def _texto_obligatorio(valor, nombre_campo):
        if valor is None:
            raise ValueError(f"{nombre_campo} es obligatorio")
        valor = str(valor).strip()
        if not valor:
            raise ValueError(f"{nombre_campo} no puede estar vacío")
        return valor

    @staticmethod
    def crear_cargo(cargo: Cargo):
        if hasattr(cargo, "descripcion"):
            cargo.descripcion = CargoService._texto_obligatorio(cargo.descripcion, "descripcion")
        elif hasattr(cargo, "nombre"):
            cargo.nombre = CargoService._texto_obligatorio(cargo.nombre, "nombre")
        return CargoRepository.crear(cargo)

    @staticmethod
    def buscar_por_id(id: int) -> Cargo:
        return CargoRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[Cargo]:
        return CargoRepository.buscar_todos()

    @staticmethod
    def actualizar_cargo(id: int, cargo: Cargo) -> Cargo:
        cargo_existente = CargoRepository.buscar_por_id(id)
        if not cargo_existente:
            return None

        if hasattr(cargo_existente, "descripcion") and hasattr(cargo, "descripcion"):
            cargo_existente.descripcion = CargoService._texto_obligatorio(cargo.descripcion, "descripcion")
        elif hasattr(cargo_existente, "nombre") and hasattr(cargo, "nombre"):
            cargo_existente.nombre = CargoService._texto_obligatorio(cargo.nombre, "nombre")

        if hasattr(cargo_existente, "puntos") and hasattr(cargo, "puntos"):
            cargo_existente.puntos = cargo.puntos

        return CargoRepository.actualizar_cargo(cargo_existente)

    @staticmethod
    def borrar_por_id(id: int) -> Cargo:
        return CargoRepository.borrar_por_id(id)

