import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_hashids import Hashids
from sqlalchemy import event
from app.config import config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
hashids = Hashids()

def create_app() -> Flask:
    app = Flask(__name__)
    app_context = os.getenv('FLASK_CONTEXT', 'development')
    app.config.from_object(config.factory(app_context))

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    hashids.init_app(app)

    # --- Airbag: completa 'descripcion' si falta ---
    @event.listens_for(db.session.__class__, "before_flush", propagate=True)
    def _auto_fill_descripcion(session, flush_context, instances):
        for obj in session.new:
            if hasattr(obj, "nombre") and hasattr(obj, "descripcion"):
                desc = getattr(obj, "descripcion", None)
                if desc is None or not str(desc).strip():
                    setattr(obj, "descripcion", (getattr(obj, "nombre", "") or "").strip())

    # --- Blueprints ---
    from app.resources import (
        home,
        universidad_bp,
        area_bp,
        tipodocumento_bp,
        tipodedicacion_bp,
        categoriacargo_bp,
        grupo_bp,
        grado_bp,
        departamento_bp,
        certificado_bp,
        tipo_especialidad_bp,
        plan_bp,
        cargo_bp,
        alumno_bp
    )

    app.register_blueprint(home, url_prefix="/sys")
    app.register_blueprint(universidad_bp, url_prefix="/sys")
    app.register_blueprint(area_bp, url_prefix="/sys")
    app.register_blueprint(tipodocumento_bp, url_prefix="/sys")
    app.register_blueprint(tipodedicacion_bp, url_prefix="/sys")
    app.register_blueprint(categoriacargo_bp, url_prefix="/sys")
    app.register_blueprint(grupo_bp, url_prefix="/sys")
    app.register_blueprint(grado_bp, url_prefix="/sys")
    app.register_blueprint(departamento_bp, url_prefix="/sys")
    app.register_blueprint(certificado_bp, url_prefix="/sys")
    app.register_blueprint(tipo_especialidad_bp, url_prefix="/sys")
    app.register_blueprint(plan_bp, url_prefix="/sys")
    app.register_blueprint(cargo_bp, url_prefix="/sys")
    app.register_blueprint(alumno_bp, url_prefix="/sys")

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
