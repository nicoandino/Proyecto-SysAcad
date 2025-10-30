import os
import pandas as pd
from datetime import date

# 📂 Carpeta destino
OUTPUT_DIR = "csv_datos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------------------------------
# 1️⃣ PAISES
# ------------------------------------------------------
paises = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "nombre": ["Argentina", "Chile", "Uruguay", "Brasil", "Paraguay"]
})
paises.to_csv(f"{OUTPUT_DIR}/paises.csv", index=False)

# ------------------------------------------------------
# 2️⃣ UNIVERSIDADES
# ------------------------------------------------------
universidades = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "nombre": [
        "Universidad Tecnológica Nacional",
        "Universidad de Mendoza",
        "Universidad de Buenos Aires",
        "Universidad Nacional de Cuyo",
        "Universidad de Córdoba"
    ],
    "sigla": ["UTN", "UM", "UBA", "UNC", "UNCOR"]
})
universidades.to_csv(f"{OUTPUT_DIR}/universidades.csv", index=False)

# ------------------------------------------------------
# 3️⃣ TIPOS DE DOCUMENTO
# ------------------------------------------------------
tipodocumentos = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "sigla": ["DNI", "LE", "LC", "PAS", "CUIT"],
    "nombre": ["Documento Nacional", "Libreta de Enrolamiento", "Libreta Cívica", "Pasaporte", "CUIT"],
    "descripcion": ["Documento oficial"] * 5
})
tipodocumentos.to_csv(f"{OUTPUT_DIR}/tipodocumentos.csv", index=False)

# ------------------------------------------------------
# 4️⃣ TIPO DE ESPECIALIDAD
# ------------------------------------------------------
tipoespecialidades = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "nombre": ["Ingeniería", "Tecnicatura", "Licenciatura", "Maestría", "Doctorado"],
    "nivel": ["Avanzado"] * 5
})
tipoespecialidades.to_csv(f"{OUTPUT_DIR}/tipoespecialidades.csv", index=False)

# ------------------------------------------------------
# 5️⃣ FACULTADES (FK universidad)
# ------------------------------------------------------
facultades = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "facultad": [0, 0, 0, 0, 0],
    "nombre": [
        "Facultad Regional Mendoza",
        "Facultad Regional Buenos Aires",
        "Facultad Regional San Rafael",
        "Facultad Regional Córdoba",
        "Facultad Regional Rosario"
    ],
    "universidad_id": [1, 1, 1, 1, 1]
})
facultades.to_csv(f"{OUTPUT_DIR}/facultades.csv", index=False)

# ------------------------------------------------------
# 6️⃣ ESPECIALIDADES (FK tipoespecialidad + facultad)
# ------------------------------------------------------
especialidades = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "nombre": [
        "Ingeniería en Sistemas",
        "Ingeniería Electrónica",
        "Ingeniería Civil",
        "Ingeniería Industrial",
        "Ingeniería Química"
    ],
    "letra": ["A", "B", "C", "D", "E"],
    "observacion": ["Plan vigente"] * 5,
    "tipoespecialidad_id": [1, 1, 1, 1, 1],
    "facultad_id": [1, 2, 3, 4, 5]
})
especialidades.to_csv(f"{OUTPUT_DIR}/especialidades.csv", index=False)

# ------------------------------------------------------
# 7️⃣ MATERIAS
# ------------------------------------------------------
materias = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "nombre": ["Matemática", "Física", "Programación", "Base de Datos", "Economía"],
    "codigo": ["MAT101", "FIS101", "PRO101", "BD101", "ECO101"],
    "observacion": ["Troncal"] * 5
})
materias.to_csv(f"{OUTPUT_DIR}/materias.csv", index=False)

# ------------------------------------------------------
# 8️⃣ PLANES (FK especialidad)
# ------------------------------------------------------
planes = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "nombre": ["Plan 2019", "Plan 2020", "Plan 2021", "Plan 2022", "Plan 2023"],
    "fecha_inicio": [date(2019, 3, 1), date(2020, 3, 1), date(2021, 3, 1), date(2022, 3, 1), date(2023, 3, 1)],
    "fecha_fin": [None] * 5,
    "observacion": ["Plan activo"] * 5,
    "anio": [2019, 2020, 2021, 2022, 2023],
    "especialidad_id": [1, 2, 3, 4, 5]
})
planes.to_csv(f"{OUTPUT_DIR}/planes.csv", index=False)

# ------------------------------------------------------
# 9️⃣ CARGOS
# ------------------------------------------------------
cargos = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "nombre": ["Profesor", "Jefe de Cátedra", "Ayudante", "Asistente", "Investigador"],
    "descripcion": ["Sin descripción"] * 5,
    "grado": [1, 2, 3, 4, 5],
    "categoria_cargo_id": [None] * 5,
    "tipo_dedicacion_id": [None] * 5
})
cargos.to_csv(f"{OUTPUT_DIR}/cargos.csv", index=False)

# ------------------------------------------------------
# 🔟 AUTORIDADES (FK cargo + tipo_documento)
# ------------------------------------------------------
autoridades = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "nombre": ["Juan Pérez", "María López", "Carlos Gómez", "Laura Torres", "Pedro Sánchez"],
    "telefono": ["123456789"] * 5,
    "email": [
        "jperez@mail.com", "mlopez@mail.com", "cgomez@mail.com", "ltorres@mail.com", "psanchez@mail.com"
    ],
    "cargo_id": [1, 2, 3, 4, 5],
    "tipo_documento_id": [1, 1, 1, 1, 1]
})
autoridades.to_csv(f"{OUTPUT_DIR}/autoridades.csv", index=False)

# ------------------------------------------------------
# 1️⃣1️⃣ ALUMNOS (FK facultad + tipo_documento + especialidad + pais)
# ------------------------------------------------------
alumnos = pd.DataFrame({
    "nro_legajo": [1, 2, 3, 4, 5],
    "apellido": ["Andino", "López", "Martínez", "Suárez", "Gómez"],
    "nombre": ["Nicolás", "Ezequiel", "Matías", "Lucas", "Mariana"],
    "nro_documento": [40111222, 40222333, 40333444, 40444555, 40555666],
    "fecha_nacimiento": [
        date(2000, 1, 1), date(1999, 2, 2), date(1998, 3, 3), date(1997, 4, 4), date(1996, 5, 5)
    ],
    "sexo": ["M", "M", "M", "M", "F"],
    "fecha_ingreso": [
        date(2020, 3, 1), date(2020, 3, 1), date(2021, 3, 1), date(2021, 3, 1), date(2022, 3, 1)
    ],
    "facultad_id": [1, 1, 2, 3, 4],
    "especialidad_id": [1, 2, 3, 4, 5],
    "tipo_documento_id": [1, 1, 1, 1, 1],
    "pais_id": [1, 1, 1, 1, 1]
})
alumnos.to_csv(f"{OUTPUT_DIR}/alumnos.csv", index=False)

print("✅ CSV generados correctamente en la carpeta 'csv_datos/'")
