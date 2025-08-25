from flask import Blueprint

tipodedicacion_bp = Blueprint("tipodedicacion", __name__)

@tipodedicacion_bp.route("/tipodedicacion/test", methods=["GET"])
def tipodedicacion_test():
    return {"msg": "TipoDedicacion funcionando correctamente"}
