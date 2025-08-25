from marshmallow import fields, Schema, post_load, validate
from app.models import Alumno

class AlumnoMapping(Schema):
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=100))
    apellido = fields.String(required=True, validate=validate.Length(min=1, max=100))
    nro_documento = fields.String(required=True, validate=validate.Length(equal=8))
    sexo = fields.String(required=True, validate=validate.Length(equal=1))
    nro_legajo = fields.Integer(required=True)
    fecha_nacimiento = fields.Date(required=True)
    fecha_ingreso = fields.Date(required=True)

    @post_load
    def make_alumno(self, data, **kwargs) -> Alumno:
        return Alumno(**data)
