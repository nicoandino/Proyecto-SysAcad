from datetime import date
from app.models import (
    Universidad, Facultad, Departamento, Materia, Plan,
    Especialidad, TipoEspecialidad, Orientacion, Pais,
    Cargo, CategoriaCargo, Autoridad, Alumno,
    Area, Grado, Grupo, TipoDedicacion, TipoDocumento
)

# Universidad
def nuevauniversidad(**kwargs):
    return Universidad(
        nombre=kwargs.get("nombre", "Universidad Nacional de San Rafael")
    )

# test/instancias.py
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

def nueva_materia(**kwargs) -> Materia:
    return Materia(
        nombre=kwargs.get("nombre", "Matematica"),
        codigo=kwargs.get("codigo", "MAT101"),
        observacion=kwargs.get("observacion", "Matematica basica"),
    )

# ✅ Crea y persiste en DB una Materia (con Especialidad dummy si no se pasa)
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

# 🔁 Alias para compatibilidad con tests que importan "nuevamateria"
def nuevamateria(**kwargs):
    return nueva_materia(**kwargs)
# Plan
def nuevoplan(**kwargs):
    return Plan(
        especialidad=kwargs.get("especialidad"),
        plan=kwargs.get("plan", 2020),
        nombre=kwargs.get("nombre", "Plan de Ingeniería")
    )

from app.models import Especialidad, TipoEspecialidad
from app.services import EspecialidadService, TipoEspecialidadService


# ---------- Tipo Especialidad ----------
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
def nuevaorientacion(**kwargs):
    return Orientacion(
        especialidad=kwargs.get("especialidad"),
        plan=kwargs.get("plan"),
        orientacion=kwargs.get("orientacion", "OR1"),
        nombre=kwargs.get("nombre", "Orientación General")
    )

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
def nuevotipodedicacion(**kwargs):
    return TipoDedicacion(
        nombre=kwargs.get("nombre", "Exclusiva")
    )

# Tipo Documento
def nuevotipodocumento(**kwargs):
    return TipoDocumento(
        dni=kwargs.get("dni", 50291002),
        libreta_civica=kwargs.get("libreta_civica", "LC"),
        libreta_enrolamiento=kwargs.get("libreta_enrolamiento", "LE"),
        pasaporte=kwargs.get("pasaporte", "PAS")
    )
