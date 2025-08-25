from flask import Blueprint

tipodocumento_bp = Blueprint("tipodocumento", __name__)

@tipodocumento_bp.route("/tipodocumento/test", methods=["GET"])
def tipodocumento_test():
    return {"msg": "TipoDocumento funcionando correctamente"}
