# scripts/ejecutar_importaciones.py

import sys
import os

# --- Bootstrap path del proyecto ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# App / DB
from app import create_app, db

# Importadores (ajusta nombres si difieren)
from import_especialidades import importar_especialidades
from import_facultades import importar_facultades
from import_grados import importar_grados
from import_paises import importar_paises
from import_localidades import importar_localidades
from import_planes import importar_planes
from import_materias import importar_materias
from import_orientaciones import importar_orientaciones
from import_universidad import importar_universidades
from insert_alumnos import importar_alumnos

def _run(step_name, fn):
    print(f"\n>>> {step_name} ...")
    try:
        fn()
        print(f">>> {step_name} ✔")
    except Exception as e:
        # No frenamos la corrida completa si un import falla
        print(f">>> {step_name} ✖  Error: {e}")


def ejecutar_todo():
    print(">>> Iniciando proceso de importación de datos XML...\n")
    os.environ['FLASK_CONTEXT'] = 'development'
    app = create_app()
    with app.app_context():
        # 1) Crear tablas si no existen
        print(">>> Creando tablas (db.create_all()) si no existen...")
        db.create_all()
        print(">>> Tablas OK.\n")

        # 2) Ejecutar importadores en orden seguro
        #    - Primero entidades base (catálogos)
        _run("Importar ESPECIALIDADES", importar_especialidades)
        _run("Importar FACULTADES", importar_facultades)
        _run("Importar GRADOS", importar_grados)
        _run("Importar PAISES", importar_paises)
        _run("Importar LOCALIDADES", importar_localidades)

        #    - Luego PLANES (antes que ORIENTACIONES)
        _run("Importar PLANES", importar_planes)

        #    - Luego MATERIAS (si dependen de especialidad/plan)
        _run("Importar MATERIAS", importar_materias)

        #    - Luego ORIENTACIONES (requiere PLANES creados)
        _run("Importar ORIENTACIONES", importar_orientaciones)

        #    - Finalmente UNIVERSIDADES (independiente, o al final por prolijidad)
        _run("Importar UNIVERSIDADES", importar_universidades)

        _run("Importar ALUMNOS", importar_alumnos)
    print("\n>>> Proceso de importación finalizado.")


if __name__ == "__main__":
    ejecutar_todo()
