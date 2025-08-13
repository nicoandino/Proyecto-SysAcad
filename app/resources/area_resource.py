from flask import Blueprint

area_bp = Blueprint("area", __name__)

@area_bp.route("/area/test", methods=["GET"])
def area_test():
    return {"msg": "Área funcionando correctamente"}
