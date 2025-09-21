# app/resources/universidad_resource.py
from flask import jsonify, Blueprint, request
from app.mapping.universidad_mapping import UniversidadMapping
from app.services.universidad_service import UniversidadService

universidad_bp = Blueprint('universidad', __name__)

@universidad_bp.route('/universidad', methods=['GET'])
def buscar_todos():
    universidades = UniversidadService.buscar_todos()
    data = UniversidadMapping(many=True).dump(universidades)   # <- many=True
    return jsonify(data), 200

@universidad_bp.route('/universidad/<int:id>', methods=['GET'])
def buscar_por_id(id):
    u = UniversidadService.buscar_por_id(id)
    if not u:
        return jsonify({"message": "No encontrada"}), 404
    data = UniversidadMapping(many=False).dump(u)              # <- many=False
    return jsonify(data), 200

@universidad_bp.route('/universidad', methods=['POST'])
def crear():
    obj = UniversidadMapping(many=False).load(request.get_json())
    creada = UniversidadService.crear(obj)
    data = UniversidadMapping(many=False).dump(creada)
    return jsonify(data), 201

@universidad_bp.route('/universidad/<int:id>', methods=['PUT'])
def actualizar(id):
    existente = UniversidadService.buscar_por_id(id)
    if not existente:
        return jsonify({"error": "Universidad no encontrada"}), 404
    actualizado = UniversidadMapping(many=False).load(request.get_json(), instance=existente, partial=True)
    out = UniversidadService.actualizar(id, actualizado)
    data = UniversidadMapping(many=False).dump(out)
    return jsonify(data), 200

@universidad_bp.route('/universidad/<int:id>', methods=['DELETE'])
def borrar_por_id(id):
    ok = UniversidadService.borrar_por_id(id)
    if not ok:
        return jsonify({"error": "Universidad no encontrada"}), 404
    return jsonify({"message": "Universidad borrada exitosamente"}), 200
