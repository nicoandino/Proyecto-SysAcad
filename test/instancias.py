from datetime import date
from app.models import (
    Universidad, Facultad, Departamento, Materia, Plan,
    Especialidad, TipoEspecialidad, Orientacion, Pais,
    Cargo, CategoriaCargo, Autoridad, Alumno
)

#  Universidad
def nuevauniversidad(**kwargs):
    return Universidad(
        nombre=kwargs.get("nombre", "Universidad Nacional de San Rafael")
    )

#  Facultad
def nuevafacultad(**kwargs):
    return Facultad(
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
        codigo=kwargs.get("codigo")
    )

#  Departamento
def nuevodepartamento(**kwargs):
    return Departamento(
        nombre=kwargs.get("nombre", "Departamento Genérico")
    )

#  Materia
def nuevamateria(**kwargs):
    return Materia(
        especialidad=kwargs.get("especialidad", "INF"),
        plan=kwargs.get("plan", "2020"),
        materia=kwargs.get("materia", "MAT101"),
        nombre=kwargs.get("nombre", "Álgebra"),
        ano=kwargs.get("ano", 1),
        observacion=kwargs.get("observacion", "Obligatoria")
    )

#  Plan
def nuevoplan(**kwargs):
    return Plan(
        especialidad=kwargs.get("especialidad", "INF"),
        plan=kwargs.get("plan", 2020),
        nombre=kwargs.get("nombre", "Plan de Ingeniería")
    )

#  Especialidad
def nuevaespecialidad(**kwargs):
    tipo = kwargs.get("tipoespecialidad") or TipoEspecialidad(nombre="Cardiología")
    return Especialidad(
        nombre=kwargs.get("nombre", "Matemáticas"),
        letra=kwargs.get("letra", "A"),
        tipoespecialidad_id=kwargs.get("tipoespecialidad_id", tipo.id),
        tipoespecialidad=tipo
    )

#  Orientación
def nuevaorientacion(**kwargs):
    return Orientacion(
        especialidad=kwargs.get("especialidad", "INF"),
        plan=kwargs.get("plan", "2020"),
        orientacion=kwargs.get("orientacion", "OR1"),
        nombre=kwargs.get("nombre", "Orientación General")
    )

#  País
def nuevopais(**kwargs):
    return Pais(
        pais=kwargs.get("pais", 1),
        nombre=kwargs.get("nombre", "Argentina")
    )

#  Cargo
def nuevacargo(**kwargs):
    return Cargo(
        nombre=kwargs.get("nombre", "Director"),
        grado=kwargs.get("grado", 1),
        descripcion=kwargs.get("descripcion", "Sin descripción")
    )

# Categoría de Cargo
def nuevacategoriacargo(**kwargs):
    return CategoriaCargo(
        nombre=kwargs.get("nombre", "Docente")
    )

#  Autoridad
def nuevaautoridad(**kwargs):
    autoridad = Autoridad(
        nombre=kwargs.get("nombre", "Pelo"),
        telefono=kwargs.get("telefono", "123456789"),
        email=kwargs.get("email", "pelo@example.com"),
        cargo_id=kwargs.get("cargo_id")
    )
    if "materias" in kwargs:
        autoridad.materias.extend(kwargs["materias"])
    if "facultades" in kwargs:
        autoridad.facultades.extend(kwargs["facultades"])
    return autoridad

# Alumno
def nuevoalumno(**kwargs):
    datos = {
        "nombre": "Juan",
        "apellido": "Pérez",
        "nro_documento": 12345678,
        "tipo_documento": "DNI",
        "fecha_nacimiento": date(2000, 1, 1),
        "sexo": "M",
        "nro_legajo": 1001,
        "fecha_ingreso": date(2022, 3, 1)
    }
    datos.update(kwargs)
    return Alumno(**datos)
