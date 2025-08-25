from flask import jsonify, Blueprint, request

from app.mapping.alumno_mapping import AlumnoMapping
from app.services.alumno_service import AlumnoService

alumno_bp = Blueprint('alumno', __name__)
alumno_mapping = AlumnoMapping()

@alumno_bp.route('/alumno', methods=['GET'])
def buscar_todos():
    alumnos = AlumnoService.buscar_todos()
    return alumno_mapping.dump(alumnos, many=True), 200

@alumno_bp.route('/alumno/<int:nro_legajo>', methods=['GET'])
def buscar_por_id(nro_legajo):
    alumno = AlumnoService.buscar_por_id(nro_legajo)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404
    return alumno_mapping.dump(alumno), 200

@alumno_bp.route('/alumno', methods=['POST'])
def crear():
    alumno = alumno_mapping.load(request.get_json())
    AlumnoService.crear(alumno)
    return jsonify({"message": "Alumno creado exitosamente"}), 201

@alumno_bp.route('/alumno/<int:nro_legajo>', methods=['PUT'])
def actualizar(nro_legajo):
    alumno = AlumnoService.buscar_por_id(nro_legajo)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404

    data = request.get_json()
    alumno_actualizado = alumno_mapping.load(data, instance=alumno, partial=True)
    AlumnoService.actualizar(alumno_actualizado)
    return jsonify({"message": "Alumno actualizado exitosamente"}), 200

@alumno_bp.route('/alumno/<int:nro_legajo>', methods=['DELETE'])
def borrar_por_id(nro_legajo):
    alumno = AlumnoService.buscar_por_id(nro_legajo)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404

    AlumnoService.borrar_por_id(nro_legajo)
    return jsonify({"message": "Alumno borrado exitosamente"}), 200
