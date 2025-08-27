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

# Facultad
def nuevafacultad(**kwargs):
    from app import db
    from app.models.universidad import Universidad

    # Si no te pasan universidad, creamos una dummy
    universidad = kwargs.get("universidad")
    if not universidad:
        universidad = Universidad(nombre="Universidad X")
        db.session.add(universidad)
        db.session.commit()

    facultad = Facultad(
        facultad=kwargs.get("facultad", 0),  # campo obligatorio
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
        universidad=universidad
    )

    db.session.add(facultad)
    db.session.commit()  # 🔹 genera el ID
    return facultad


# Departamento
def nuevodepartamento(**kwargs):
    return Departamento(
        nombre=kwargs.get("nombre", "Departamento Genérico")
    )

# Área
from app import db
from app.models.area import Area


def nuevaarea(nombre="Area Académica", **kwargs):
    area = Area(nombre=nombre)
    db.session.add(area)
    db.session.commit()
    return area
# Grado
def nuevogrado(**kwargs):
    return Grado(
        nombre=kwargs.get("nombre", "Licenciatura")
    )

# Grupo
def nuevogrupo(**kwargs):
    return Grupo(
        nombre=kwargs.get("nombre", "Grupo 1")
    )

# Materia
def nuevamateria(**kwargs):
    especialidad = kwargs.get("especialidad")
    if not especialidad:
        # Creamos una especialidad dummy para no violar el FK
        especialidad = Especialidad(nombre="Especialidad Test")
        db.session.add(especialidad)
        db.session.commit()

    materia = Materia(
        nombre=kwargs.get("nombre", "Álgebra"),
        codigo=kwargs.get("codigo", "MAT101"),
        observacion=kwargs.get("observacion", "Obligatoria"),
        especialidad_id=especialidad.id   # ✅ se guarda el FK válido
    )
    db.session.add(materia)
    db.session.commit()   # ✅ ahora materia.id ya no es None
    return materia

# Plan
def nuevoplan(**kwargs):
    return Plan(
        especialidad=kwargs.get("especialidad"),
        plan=kwargs.get("plan", 2020),
        nombre=kwargs.get("nombre", "Plan de Ingeniería")
    )

# Tipo Especialidad
def nuevotipoespecialidad(**kwargs):
    return TipoEspecialidad(
        nombre=kwargs.get("nombre", "General")
    )

# Especialidad
def nuevaespecialidad(**kwargs):
    tipo = kwargs.get("tipoespecialidad") or nuevotipoespecialidad()
    return Especialidad(
        nombre=kwargs.get("nombre", "Matemáticas"),
        letra=kwargs.get("letra", "A"),
        tipoespecialidad=tipo
    )

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
    return CategoriaCargo(
        nombre=kwargs.get("nombre", "Docente")
    )

#Cargo
def nuevocargo(**kwargs):
    cargo = Cargo(
        nombre=kwargs.get("nombre", "Cargo de prueba"),
        descripcion=kwargs.get("descripcion", "Sin descripción"),
        grado=kwargs.get("grado"),
        categoria_cargo=kwargs.get("categoria_cargo"),
        tipo_dedicacion=kwargs.get("tipo_dedicacion")
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
