# app/resources/certificado_resource.py
from flask import Blueprint, send_file, abort
from app.services.alumno_service import AlumnoService

certificado_bp = Blueprint("certificado", __name__)

@certificado_bp.route("/certificado/<int:id>/docx", methods=["GET"])
def certificado_en_docx(id: int):
    # Genera (buffer, filename) o None si no existe el alumno
    res = AlumnoService.generar_certificado_alumno_regular_docx(id)
    if not res:
        abort(404, description="Alumno no encontrado")

    buffer, filename = res
    return send_file(
        buffer,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        as_attachment=True,
        download_name=filename,
    )
