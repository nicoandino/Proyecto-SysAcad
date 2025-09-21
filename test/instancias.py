from datetime import date
from app.models import (
    Universidad, Facultad, Departamento, Materia, Plan,
    Especialidad, TipoEspecialidad, Orientacion, Pais,
    Cargo, CategoriaCargo, Autoridad, Alumno,
    Area, Grado, Grupo, TipoDedicacion, TipoDocumento
)

def nuevauniversidad(**kwargs):
    u = Universidad(
        nombre=kwargs.get("nombre", "Universidad Nacional"),
        sigla=kwargs.get("sigla", "UN")   # obligatorio por el Schema
    )
    db.session.add(u)
    db.session.commit()   # 🔹 asegura que tenga id
    return u
# Facultad
from app import db
from app.models import Facultad, Universidad

def nuevafacultad(**kwargs):
    universidad = kwargs.get("universidad")
    if not universidad:
        universidad = Universidad(nombre=kwargs.get("universidad_nombre", "Universidad Nacional"))
        db.session.add(universidad)
        db.session.flush()

    facultad = Facultad(
        facultad=kwargs.get("facultad", 0),
        nombre=kwargs.get("nombre", "Facultad de Ciencias"),
        abreviatura=kwargs.get("abreviatura"),
        directorio=kwargs.get("directorio"),
        sigla=kwargs.get("sigla"),
        codigo_postal=kwargs.get("codigo_postal"),
        ciudad=kwargs.get("ciudad"),
        domicilio=kwargs.get("domicilio"),
        telefono=kwargs.get("telefono"),
        contacto=kwargs.get("contacto"),
        email=kwargs.get("email"),
        universidad=universidad,
    )

    # 🔹 Asociar autoridades si vienen por parámetro
    autoridades = kwargs.get("autoridades") or []
    for aut in autoridades:
        facultad.autoridades.append(aut)   # o facultad.asociar_autoridad(aut)

    db.session.add(facultad)
    db.session.commit()
    return facultad

# Departamento
def nuevodepartamento(nombre="Matematicas"):
    from app.models import Departamento
    from app.services import DepartamentoService
    dep = Departamento(nombre=nombre)
    return DepartamentoService.crear(dep)

# Área
from app import db
from app.models.area import Area


def nuevaarea(nombre="Area Académica", **kwargs):
    area = Area(nombre=nombre)
    db.session.add(area)
    db.session.commit()
    return area
# Grado
# test/instancias.py
from app import db
from app.models.grado import Grado

def nuevogrado(**kwargs):
    g = Grado(
        grado=kwargs.get("grado", 0),
        nombre=kwargs.get("nombre", "Primero"),
        descripcion=kwargs.get("descripcion", "Descripcion del primer grado")  # <- clave
    )
    db.session.add(g)
    db.session.commit()
    return g

# Grupo
def nuevogrupo(**kwargs):
    g = Grupo(
        nombre=kwargs.get("nombre", "Grupo A")   # el test espera "Grupo A"
    )
    db.session.add(g)
    db.session.commit()  # guarda en la DB y asigna id
    return g

# Materia
from app.services import MateriaService

# Mantener estas dos funciones como estaban:
def nueva_materia(**kwargs) -> Materia:
    return Materia(
        nombre=kwargs.get("nombre", "Matematica"),
        codigo=kwargs.get("codigo", "MAT101"),
        observacion=kwargs.get("observacion", "Matematica basica"),
    )

def crear_materia_persistida(**kwargs) -> Materia:
    especialidad = kwargs.get("especialidad")
    if not especialidad:
        especialidad = Especialidad(nombre="Especialidad Test")
        db.session.add(especialidad)
        db.session.commit()

    materia = Materia(
        nombre=kwargs.get("nombre", "Matematica"),
        codigo=kwargs.get("codigo", "MAT101"),
        observacion=kwargs.get("observacion", "Matematica basica"),
        especialidad_id=especialidad.id,
    )
    return MateriaService.crear_materia(materia)

# 🔁 Cambiar el alias para que devuelva la versión PERSISTIDA:
def nuevamateria(**kwargs):
    return crear_materia_persistida(**kwargs)

# Plan

def nuevoplan(*args, **kwargs) -> Plan:
    if args:
        # Posicional: (nombre, fecha_inicio, fecha_fin, observacion)
        nombre = args[0] if len(args) > 0 else "Plan A"
        fecha_inicio = args[1] if len(args) > 1 else None
        fecha_fin = args[2] if len(args) > 2 else None
        observacion = args[3] if len(args) > 3 else None
    else:
        nombre = kwargs.get("nombre", "Plan A")
        fecha_inicio = kwargs.get("fecha_inicio")
        fecha_fin = kwargs.get("fecha_fin")
        observacion = kwargs.get("observacion")

    # especialidad opcional (como objeto o id)
    especialidad = kwargs.get("especialidad")
    especialidad_id = kwargs.get("especialidad_id")
    if especialidad and not especialidad_id:
        especialidad_id = getattr(especialidad, "id", None)
        if especialidad_id is None:
            db.session.add(especialidad)
            db.session.flush()
            especialidad_id = especialidad.id

    plan = Plan(
        nombre=nombre,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        observacion=observacion,
        anio=kwargs.get("anio"),
        especialidad_id=especialidad_id
    )

    db.session.add(plan)
    db.session.flush()
    db.session.commit()
    return plan



# ---------- Tipo Especialidad ----------

from app.models import Especialidad, TipoEspecialidad
from app.services import EspecialidadService, TipoEspecialidadService

def nuevotipoespecialidad(**kwargs):
    tipo = TipoEspecialidad(
        nombre=kwargs.get("nombre", "Cardiologia")
    )
    return TipoEspecialidadService.crear(tipo)   # devuelve instancia con id


# ---------- Especialidad ----------
def nuevaespecialidad(**kwargs):
    tipo = kwargs.get("tipoespecialidad") or nuevotipoespecialidad(nombre="Cardiologia")
    especialidad = Especialidad(
        nombre=kwargs.get("nombre", "Matematicas"),  # sin tilde para pasar test
        letra=kwargs.get("letra", "A"),
        tipoespecialidad=tipo                       # relación, no mezclar con *_id
    )
    return EspecialidadService.crear(especialidad)  # devuelve instancia persistida con id

# Orientación
def nuevaorientacion(**kwargs) -> Orientacion:
    # --- TipoEspecialidad ---
    tipo = kwargs.get("tipoespecialidad")
    if not tipo:
        tipo = TipoEspecialidad(nombre="Cardiologia")
        db.session.add(tipo)
        db.session.flush()

    # --- Especialidad ---
    especialidad = kwargs.get("especialidad")
    if not especialidad:
        especialidad = Especialidad(
            nombre=kwargs.get("nombre_especialidad", "Especialidad Test"),
            letra=kwargs.get("letra_especialidad", "A"),
            tipoespecialidad=tipo
        )
        db.session.add(especialidad)
        db.session.flush()

    # --- Plan ---
    plan = kwargs.get("plan")
    if not plan:
        plan = Plan(
            nombre=kwargs.get("nombre_plan", "Plan 2024"),
            fecha_inicio=kwargs.get("fecha_inicio_plan", date(2024, 6, 4))
        )
        db.session.add(plan)
        db.session.flush()

    # --- Materia ---
    materia = kwargs.get("materia")
    if not materia:
        materia = Materia(
            nombre=kwargs.get("nombre_materia", "Desarrollo"),
            codigo=kwargs.get("codigo_materia", "DES101"),
            observacion=kwargs.get("obs_materia", "Materia de desarrollo")
        )
        db.session.add(materia)
        db.session.flush()

    # --- Orientacion ---
    orientacion = Orientacion(
        nombre=kwargs.get("nombre", "Orientacion 1"),
        especialidad_id=especialidad.id,
        plan_id=plan.id,
        materia_id=materia.id
    )
    db.session.add(orientacion)
    db.session.commit()

    return orientacion

# País
def nuevopais(**kwargs):
    return Pais(
        nombre=kwargs.get("nombre", "Argentina")
    )

# Cargo
def nuevacargo(**kwargs):
    return Cargo(
        nombre=kwargs.get("nombre", "Director"),
        descripcion=kwargs.get("descripcion", "Sin descripción")
    )

# Categoría de Cargo
def nuevacategoriacargo(**kwargs):
    categoria = CategoriaCargo(
        nombre=kwargs.get("nombre", "Docente")
    )
    db.session.add(categoria)
    db.session.commit()
    return categoria

#Cargo
def nuevocargo(**kwargs):
    categoria = kwargs.get("categoria_cargo") or nuevacategoriacargo()
    dedicacion = kwargs.get("tipo_dedicacion") or nuevotipodedicacion(nombre="Dedicacion Completa")
    cargo = Cargo(
        nombre=kwargs.get("nombre", "Profesor"),
        descripcion=kwargs.get("descripcion", "Sin descripción"),
        grado=kwargs.get("grado"),
        categoria_cargo=categoria,
        tipo_dedicacion=dedicacion
    )
    db.session.add(cargo)
    db.session.commit()
    return cargo




# Autoridad
def nuevaautoridad(**kwargs):
    cargo_id = kwargs.get("cargo_id")
    if not cargo_id:
        cargo = nuevocargo(nombre="Cargo por defecto")
        db.session.add(cargo)
        db.session.commit()
        cargo_id = cargo.id

    autoridad = Autoridad(
        nombre=kwargs.get("nombre", "Pelo"),
        telefono=kwargs.get("telefono", "123456789"),
        email=kwargs.get("email", "pelo@example.com"),
        cargo_id=cargo_id
    )
    if "materias" in kwargs:
        autoridad.materias.extend(kwargs["materias"])
    if "facultades" in kwargs:
        autoridad.facultades.extend(kwargs["facultades"])

    db.session.add(autoridad)
    db.session.commit()
    return autoridad

# Alumno
def nuevoalumno(**kwargs):
    datos = {
        "nombre": "Juan",
        "apellido": "Pérez",
        "nro_documento": 12345678,
        "tipo_documento": kwargs.get("tipo_documento", "DNI"),  # 👈 string
        "fecha_nacimiento": date(2000, 1, 1),
        "sexo": "M",
        "nro_legajo": 1001,
        "fecha_ingreso": date(2022, 3, 1)
    }
    datos.update(kwargs)
    return Alumno(**datos)

# Tipo Dedicación

def nuevotipodedicacion(*args, **kwargs) -> TipoDedicacion:
    if args:
        nombre = args[0] if len(args) > 0 else "Dedicacion Completa"
        observacion = args[1] if len(args) > 1 else "Observacion de prueba"
    else:
        nombre = kwargs.get("nombre", "Dedicacion Completa")
        observacion = kwargs.get("observacion", "Observacion de prueba")

    td = TipoDedicacion(
        nombre=nombre,
        observacion=observacion,
    )
    db.session.add(td)
    db.session.commit()   # asegura td.id
    return td


# Tipo Documento
def nuevotipodocumento(*args, **kwargs) -> TipoDocumento:
    if args:
        dni = args[0] if len(args) > 0 else 46291002
        libreta_civica = args[1] if len(args) > 1 else "nacional"
        libreta_enrolamiento = args[2] if len(args) > 2 else "LE"
        pasaporte = args[3] if len(args) > 3 else "PAS"
    else:
        dni = kwargs.get("dni", 46291002)
        libreta_civica = kwargs.get("libreta_civica", "nacional")
        libreta_enrolamiento = kwargs.get("libreta_enrolamiento", "LE")
        pasaporte = kwargs.get("pasaporte", "PAS")

    doc = TipoDocumento(
        dni=dni,
        libreta_civica=libreta_civica,
        libreta_enrolamiento=libreta_enrolamiento,
        pasaporte=pasaporte,
    )
    db.session.add(doc)
    db.session.commit()  # asegura doc.id
    return doc

# Tipo Especialidad
from app.models import TipoEspecialidad

def nuevotipoespecialidad(*args, **kwargs) -> TipoEspecialidad:
    """
    Usos:
      - nuevotipoespecialidad() -> ("Cardiologia", "Avanzado")
      - nuevotipoespecialidad(nombre, nivel)
    """
    if args:
        nombre = args[0] if len(args) > 0 else "Cardiologia"
        nivel = args[1] if len(args) > 1 else "Avanzado"
    else:
        nombre = kwargs.get("nombre", "Cardiologia")
        nivel = kwargs.get("nivel", "Avanzado")

    tipo = TipoEspecialidad(nombre=nombre, nivel=nivel)
    db.session.add(tipo)
    db.session.commit()
    return tipo