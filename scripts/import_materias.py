import os
import sys
import random
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError

# --- Bootstrap path del proyecto ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app, db
from app.models.materia import Materia
from app.models.especialidad import Especialidad  # para especialidad_id

# Intentar ambas variantes
CANDIDATES = [
    os.path.join('archivados_xml', 'materias.xml'),
    os.path.join('archivados_xml', 'materia.xml'),
]

# Configuración
BATCH_SIZE = 1000
ASSIGN_STRATEGY = "random"  # "random" o "mod"
FALLBACK_CREATE_PLACEHOLDER = True  # crea una especialidad dummy si no hay


def clean(text, maxlen=None):
    if text is None:
        return None
    s = text.strip()
    if not s:
        return None
    return s[:maxlen] if maxlen else s


def get_text(elem, maxlen=None):
    return clean(elem.text, maxlen) if elem is not None else None


def resolve_xml_path():
    for rel in CANDIDATES:
        path = os.path.abspath(os.path.join(BASE_DIR, rel))
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        f"No se encontró XML. Probé: {', '.join(CANDIDATES)} en {os.path.join(BASE_DIR, 'archivados_xml')}"
    )


def pick_especialidad_id(materia_id: int, especialidad_ids):
    if not especialidad_ids:
        return None
    if ASSIGN_STRATEGY == "mod" and materia_id is not None:
        return especialidad_ids[materia_id % len(especialidad_ids)]
    return random.choice(especialidad_ids)


def importar_materias():
    app = create_app()
    with app.app_context():
        xml_file_path = resolve_xml_path()
        print(f"Importando Materias desde: {xml_file_path}")

        # Traer IDs de especialidades
        especialidad_ids = [eid for (eid,) in db.session.query(Especialidad.id).all()]
        if not especialidad_ids and FALLBACK_CREATE_PLACEHOLDER:
            # Crear especialidad dummy (requiere facultad válida)
            # Ajustá 'facultad_id=1' a un id de facultad existente
            dummy = Especialidad(nombre="Especialidad Placeholder", facultad_id=1)
            db.session.add(dummy)
            db.session.commit()
            especialidad_ids = [dummy.id]
            print("⚠️ No había especialidades. Creada 'Especialidad Placeholder'.")

        # Parsear XML
        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"Error al parsear el archivo XML: {e}")
            return

        insertados = duplicados = errores = 0
        pending = 0

        for item in root.findall('_expxml'):
            materia_id_txt = get_text(item.find('materia'))
            nombre         = get_text(item.find('nombre'), 255)
            codigo         = get_text(item.find('codigo'), 20)
            observacion    = get_text(item.find('observacion'), 255)

            if not materia_id_txt or not nombre:
                errores += 1
                continue

            try:
                materia_id = int(materia_id_txt)
            except ValueError:
                errores += 1
                print(f"Error: 'materia' no es un entero válido: {materia_id_txt}")
                continue

            # fallback para 'codigo'
            if not codigo:
                codigo = str(materia_id)

            try:
                # Evitar duplicados
                if db.session.get(Materia, materia_id):
                    duplicados += 1
                    continue

                esp_id = pick_especialidad_id(materia_id, especialidad_ids)
                if esp_id is None:
                    raise RuntimeError("No hay especialidades disponibles para asignar 'especialidad_id'.")

                nueva = Materia(
                    id=materia_id,
                    nombre=nombre,
                    codigo=codigo,
                    observacion=observacion,
                    especialidad_id=esp_id,  # 🔴 FK obligatoria si la definiste NOT NULL
                )

                db.session.add(nueva)
                pending += 1

                if pending >= BATCH_SIZE:
                    db.session.commit()
                    pending = 0

                insertados += 1

            except IntegrityError as e:
                db.session.rollback()
                errores += 1
                print(f"Error de integridad al insertar ID {materia_id_txt}: {getattr(e, 'orig', e)}")
            except Exception as e:
                db.session.rollback()
                errores += 1
                print(f"Error procesando item (ID {materia_id_txt}): {e}")

        if pending:
            db.session.commit()

        print(f"""
Materias:
- Insertados: {insertados}
- Duplicados: {duplicados}
- Errores:    {errores}
""")


if __name__ == '__main__':
    importar_materias()
