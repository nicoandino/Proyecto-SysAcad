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

from app import db
from app.models import Universidad, Facultad, Especialidad, Materia

def crear_materia_persistida(**kwargs) -> Materia:
    especialidad = kwargs.get("especialidad")
    facultad = kwargs.get("facultad")
    facultad_id = kwargs.get("facultad_id")
    universidad = kwargs.get("universidad")
    universidad_id = kwargs.get("universidad_id")

    if especialidad is None:
        # A) Universidad: reusar si existe, si no crear una
        if universidad_id is None and universidad is None:
            universidad = Universidad.query.first()
            if universidad is None:
                universidad = Universidad(nombre=kwargs.get("universidad_nombre", "Universidad Test"))
                db.session.add(universidad)
                db.session.flush()
        if universidad_id is None and universidad is not None:
            universidad_id = universidad.id

        # B) Facultad: reusar si existe, si no crear con universidad_id
        if facultad_id is None and facultad is None:
            facultad = Facultad.query.first()
            if facultad is None:
                facultad = Facultad(
                    nombre=kwargs.get("nombre_facultad", "Facultad Test"),
                    facultad=kwargs.get("facultad_num", 0),
                    universidad_id=universidad_id,
                )
                db.session.add(facultad)
                db.session.flush()
        if facultad_id is None and facultad is not None:
            facultad_id = facultad.id

        # C) Especialidad con facultad asignada
        especialidad = Especialidad(
            nombre=kwargs.get("nombre_especialidad", "Especialidad Test"),
            facultad_id=facultad_id,
        )
        db.session.add(especialidad)
        db.session.flush()

    # D) Crear la materia y asociarla a la especialidad (N-M)
    materia = Materia(
        nombre=kwargs.get("nombre", "Matematica"),
        codigo=kwargs.get("codigo", "MAT101"),
        observacion=kwargs.get("observacion", "Matematica basica"),
    )
    materia.especialidades.append(especialidad)

    return MateriaService.crear_materia(materia)


# 🔁 Cambiar el alias para que devuelva la versión PERSISTIDA:
def nuevamateria(**kwargs):
    return crear_materia_persistida(**kwargs)

# Plan


def nuevoplan(*args, **kwargs) -> Plan:
    if args:
        nombre = args[0] if len(args) > 0 else "Plan A"
        fecha_inicio = args[1] if len(args) > 1 else None
        fecha_fin = args[2] if len(args) > 2 else None
        observacion = args[3] if len(args) > 3 else None
    else:
        nombre = kwargs.get("nombre", "Plan A")
        fecha_inicio = kwargs.get("fecha_inicio")
        fecha_fin = kwargs.get("fecha_fin")
        observacion = kwargs.get("observacion")

    # 🔹 Si no viene especialidad, la creamos completa (con facultad y universidad)
    especialidad = kwargs.get("especialidad")
    especialidad_id = kwargs.get("especialidad_id")

    if not especialidad and not especialidad_id:
        # Universidad
        universidad = Universidad(nombre="Universidad Test")
        db.session.add(universidad)
        db.session.flush()

        # Facultad
        facultad = Facultad(nombre="Facultad Test", facultad=0, universidad_id=universidad.id)
        db.session.add(facultad)
        db.session.flush()

        # Tipo de especialidad
        tipo = TipoEspecialidad(nombre="Tipo Test")
        db.session.add(tipo)
        db.session.flush()

        # Especialidad
        especialidad = Especialidad(
            nombre="Especialidad Test",
            facultad_id=facultad.id,
            tipoespecialidad_id=tipo.id
        )
        db.session.add(especialidad)
        db.session.flush()

        especialidad_id = especialidad.id

    elif especialidad and not especialidad_id:
        db.session.add(especialidad)
        db.session.flush()
        especialidad_id = especialidad.id

    # 🔹 Crear plan con especialidad obligatoria
    plan = Plan(
        nombre=nombre,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        observacion=observacion,
        anio=kwargs.get("anio"),
        especialidad_id=especialidad_id
    )

    db.session.add(plan)
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
    # 1) Tipo (dejás tu helper para "Cardiologia")
    tipo = kwargs.get("tipoespecialidad") or nuevotipoespecialidad(nombre="Cardiologia")

    # 2) Universidad (reusar si viene; si no, crear)
    universidad = kwargs.get("universidad")
    universidad_id = kwargs.get("universidad_id")
    if universidad is None and universidad_id is None:
        universidad = Universidad(nombre=kwargs.get("universidad_nombre", "Universidad Test"))
        db.session.add(universidad)
        db.session.flush()
        universidad_id = universidad.id
    elif universidad is not None and universidad_id is None:
        universidad_id = universidad.id

    # 3) Facultad (reusar si viene; si no, crear con universidad_id)
    facultad = kwargs.get("facultad")
    facultad_id = kwargs.get("facultad_id")
    if facultad is None and facultad_id is None:
        facultad = Facultad(
            nombre=kwargs.get("nombre_facultad", "Facultad Test"),
            facultad=kwargs.get("facultad_num", 0),
            universidad_id=universidad_id,
        )
        db.session.add(facultad)
        db.session.flush()
        facultad_id = facultad.id
    elif facultad is not None and facultad_id is None:
        facultad_id = facultad.id

    # 4) Especialidad con todas las FKs completas
    especialidad = Especialidad(
        nombre=kwargs.get("nombre", "Matematicas"),
        letra=kwargs.get("letra", "A"),
        tipoespecialidad=tipo,   # relación ok
        facultad_id=facultad_id  # <- clave: NOT NULL
    )

    # 5) Dejar que el Service persista
    return EspecialidadService.crear(especialidad)
def nuevaorientacion(**kwargs) -> Orientacion:
    # --- Tipo de especialidad ---
    tipo = kwargs.get("tipoespecialidad")
    if not tipo:
        tipo = TipoEspecialidad(nombre="Cardiologia")
        db.session.add(tipo)
        db.session.flush()

    # --- Universidad ---
    universidad = kwargs.get("universidad")
    if not universidad:
        universidad = Universidad(nombre="Universidad Nacional")
        db.session.add(universidad)
        db.session.flush()

    # --- Facultad ---
    facultad = kwargs.get("facultad")
    if not facultad:
        facultad = Facultad(
            nombre="Facultad de Ciencias",
            facultad=1,
            universidad_id=universidad.id
        )
        db.session.add(facultad)
        db.session.flush()

    # --- Especialidad ---
    especialidad = kwargs.get("especialidad")
    if not especialidad:
        especialidad = Especialidad(
            nombre=kwargs.get("nombre_especialidad", "Especialidad Test"),
            letra=kwargs.get("letra_especialidad", "A"),
            tipoespecialidad=tipo,
            facultad_id=facultad.id  # 👈 antes faltaba esto
        )
        db.session.add(especialidad)
        db.session.flush()

    # --- Plan ---
    plan = kwargs.get("plan")
    if not plan:
        plan = Plan(
            nombre=kwargs.get("nombre_plan", "Plan 2024"),
            fecha_inicio=kwargs.get("fecha_inicio_plan", date(2024, 6, 4)),
            especialidad_id=especialidad.id  # 👈 Esto faltaba
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

    # --- Orientación ---
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
from app.models.facultad import Facultad

def nuevoalumno(**kwargs):
    # 1️⃣ Crear o recuperar universidad
    uni = kwargs.get("universidad")
    if uni is None:
        uni = Universidad.query.first()
        if uni is None:
            uni = Universidad(nombre="Universidad Tecnológica Nacional")
            db.session.add(uni)
            db.session.commit()

    # 2️⃣ Crear o recuperar facultad
    facu = kwargs.get("facultad")
    if facu is None:
        facu = Facultad.query.first()
        if facu is None:
            facu = Facultad(nombre="Facultad de Ingeniería", universidad=uni)
            db.session.add(facu)
            db.session.commit()

    # 3️⃣ Crear o recuperar especialidad
    esp = kwargs.get("especialidad")
    if esp is None:
        esp = Especialidad.query.first()
        if esp is None:
            esp = Especialidad(nombre="Sistemas", facultad=facu)
            db.session.add(esp)
            db.session.commit()

    # 4️⃣ Crear o recuperar tipo de documento
    tipo_doc = kwargs.get("tipo_documento")
    if tipo_doc is None:
        tipo_doc = TipoDocumento.query.first()
        if tipo_doc is None:
            tipo_doc = TipoDocumento(
                sigla="DNI",
                nombre="DNI",
                descripcion="Documento Nacional de Identidad"
            )
            db.session.add(tipo_doc)
            db.session.commit()




    # 🔹 Crear o recuperar país
    pais = kwargs.get("pais")
    if pais is None:
        pais = Pais.query.first()
        if pais is None:
            pais = Pais(id=1, nombre="Argentina")  # 👈 agregar id manualmente
            db.session.add(pais)
            db.session.commit()


    datos = {
        "nombre": "Juan",
        "apellido": "Pérez",
        "nro_documento": 12345678,
        "fecha_nacimiento": date(2000, 1, 1),
        "sexo": "M",
        "nro_legajo": 1001,
        "fecha_ingreso": date(2022, 3, 1),
        "tipo_documento_id": tipo_doc.id,
        "facultad": facu,
        "especialidad": esp,
        "pais": pais,  # 👈 relación directa, no solo el ID
    }
    datos.update(kwargs)
    alumno = Alumno(**datos)
    db.session.add(alumno)
    db.session.commit()
    return alumno


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