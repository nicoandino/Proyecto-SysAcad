import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URI = os.getenv("DATABASE_URI")
engine = create_engine(DATABASE_URI)
CSV_DIR = "csv_datos"

# ✅ ORDEN CORRECTO DE CARGA
ordered_tables = [
    "paises",
    "universidades",
    "tipodocumentos",
    "tipoespecialidades",
    "facultades",
    "especialidades",
    "materias",
    "planes",
    "cargos",
    "autoridades",
    "alumnos"
]

# ------------------------------------------------------------
# FUNCIONES AUXILIARES
# ------------------------------------------------------------
def load_csv_to_db(table_name):
    path = os.path.join(CSV_DIR, f"{table_name}.csv")
    if not os.path.exists(path):
        print(f"⚠️  No se encontró {path}, se omite.")
        return

    print(f"📥 Cargando {table_name}.csv ...", end=" ")
    df = pd.read_csv(path)
    # Insertar usando COPY-like optimización (to_sql es más seguro)
    df.to_sql(table_name, engine, if_exists="append", index=False)
    print("✅ cargado correctamente.")

def disable_fk_checks(conn):
    conn.execute(text("SET session_replication_role = replica;"))

def enable_fk_checks(conn):
    conn.execute(text("SET session_replication_role = DEFAULT;"))

# ------------------------------------------------------------
# PROCESO PRINCIPAL
# ------------------------------------------------------------
with engine.begin() as conn:
    print("🚀 Deshabilitando verificaciones de FK...")
    disable_fk_checks(conn)

    for table in ordered_tables:
        load_csv_to_db(table)

    print("🔁 Rehabilitando verificaciones de FK...")
    enable_fk_checks(conn)

print("\n✅ Carga completa de CSV finalizada correctamente.")
