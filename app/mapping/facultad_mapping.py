from marshmallow import fields, Schema, post_load, validate
from app.models import Facultad

class FacultadMapping(Schema):
    id = fields.Integer(dump_only=True)
    facultad = fields.Integer(required=True)  # del nodo <facultad> en el XML
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=255))

    abreviatura = fields.String(allow_none=True, validate=validate.Length(max=50))
    sigla = fields.String(allow_none=True, validate=validate.Length(max=20))
    directorio = fields.String(allow_none=True, validate=validate.Length(max=255))
    codigo_postal = fields.String(allow_none=True, validate=validate.Length(max=20))
    ciudad = fields.String(allow_none=True, validate=validate.Length(max=120))
    domicilio = fields.String(allow_none=True, validate=validate.Length(max=255))
    telefono = fields.String(allow_none=True, validate=validate.Length(max=50))
    contacto = fields.String(allow_none=True, validate=validate.Length(max=120))

    @post_load
    def nueva_facultad(self, data, **kwargs):
        return Facultad(**data)
