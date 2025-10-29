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
from app.models.especialidad import Especialidad
from app.models.facultad import Facultad  # para facultad_id

# Intentar ambas variantes de nombre de archivo
CANDIDATES = [
    os.path.join('archivados_xml', 'especialidades.xml'),
    os.path.join('archivados_xml', 'especialidad.xml'),
]

# Configuración
BATCH_SIZE = 1000
ASSIGN_STRATEGY = "random"  # "random" o "mod" (determinista)
FALLBACK_CREATE_PLACEHOLDER = True  # crea una facultad dummy si no hay ninguna


def clean(text, maxlen=None):
    """Sanitiza textos: strip + longitud máxima."""
    if text is None:
        return None
    s = text.strip()
    if not s:
        return None
    return s[:maxlen] if maxlen else s


def get_text(elem, maxlen=None):
    """Devuelve el texto limpio de un elemento o None."""
    return clean(elem.text, maxlen) if (elem is not None and elem.text) else None


def resolve_xml_path():
    for rel in CANDIDATES:
        path = os.path.abspath(os.path.join(BASE_DIR, rel))
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        f"No se encontró XML. Probé: {', '.join(CANDIDATES)} en {os.path.join(BASE_DIR, 'archivados_xml')}"
    )


def pick_facultad_id(especialidad_id: int, facultad_ids):
    if not facultad_ids:
        return None
    if ASSIGN_STRATEGY == "mod" and especialidad_id is not None:
        return facultad_ids[especialidad_id % len(facultad_ids)]
    return random.choice(facultad_ids)


def importar_especialidades():
    app = create_app()
    with app.app_context():
        # Verificar/obtener XML
        xml_file_path = resolve_xml_path()
        print(f"Importando Especialidades desde: {xml_file_path}")

        # Traer IDs de facultades
        facultad_ids = [fid for (fid,) in db.session.query(Facultad.id).all()]
        if not facultad_ids and FALLBACK_CREATE_PLACEHOLDER:
            # Creamos una facultad dummy para no romper FK si es NOT NULL
            dummy = Facultad(nombre="Facultad Placeholder", universidad_id=1)  # ajusta si necesitas una universidad válida
            db.session.add(dummy)
            db.session.commit()
            facultad_ids = [dummy.id]
            print("⚠️ No había facultades. Creada 'Facultad Placeholder'.")

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
            especialidad_id_text = get_text(item.find('especialidad'))
            nombre        = get_text(item.find('nombre'), 100)
            letra         = get_text(item.find('letra'), 1)
            observacion   = get_text(item.find('observacion'), 255)

            if not especialidad_id_text or not nombre:
                print("Saltado: faltan 'especialidad' o 'nombre'.")
                errores += 1
                continue

            try:
                especialidad_id = int(especialidad_id_text)
            except ValueError:
                print(f"Error: 'especialidad' no es entero válido: {repr(especialidad_id_text)}")
                errores += 1
                continue

            try:
                # Evitar duplicados por PK
                if db.session.get(Especialidad, especialidad_id):
                    duplicados += 1
                    continue

                fac_id = pick_facultad_id(especialidad_id, facultad_ids)
                if fac_id is None:
                    raise RuntimeError("No hay facultades disponibles para asignar 'facultad_id'.")

                nueva = Especialidad(
                    id=especialidad_id,
                    nombre=nombre,
                    letra=letra,
                    observacion=observacion,
                    tipoespecialidad_id=None,  # ajustar si luego lo mapeás
                    facultad_id=fac_id,        # 🔴 FK obligatoria si la definiste NOT NULL
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
                print(f"Error de integridad al insertar ID {repr(especialidad_id_text)}: {getattr(e, 'orig', e)}")
            except Exception as e:
                db.session.rollback()
                errores += 1
                print(f"Error procesando ID {repr(especialidad_id_text)}: {e}")

        # Commit final
        if pending:
            db.session.commit()

        print(f"""
Especialidades:
- Insertados: {insertados}
- Duplicados: {duplicados}
- Errores:    {errores}
""")


if __name__ == '__main__':
    importar_especialidades()
