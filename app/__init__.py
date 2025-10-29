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
    app_context = os.getenv('FLASK_CONTEXT', 'testing')
    app.config.from_object(config.factory(app_context))

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    hashids.init_app(app)
    from app import models
    with app.app_context():
        db.create_all()

    # --- Airbag: completa 'descripcion' si falta ---
    @event.listens_for(db.session.__class__, "before_flush", propagate=True)
    def _auto_fill_descripcion(session, flush_context, instances):
        for obj in session.new:
            if hasattr(obj, "nombre") and hasattr(obj, "descripcion"):
                desc = getattr(obj, "descripcion", None)
                if desc is None or not str(desc).strip():
                    setattr(obj, "descripcion", (getattr(obj, "nombre", "") or "").strip())

    # --- Blueprints: importar explícitamente cada Blueprint ---
    from app.resources.home import home as home_bp
    from app.resources.universidad_resource import universidad_bp
    from app.resources.area_resource import area_bp
    from app.resources.tipodocumento_resource import tipodocumento_bp
    from app.resources.tipodedicacion_resource import tipodedicacion_bp
    from app.resources.categoriacargo_resource import categoriacargo_bp
    from app.resources.grupo_resource import grupo_bp
    from app.resources.grado_resource import grado_bp
    from app.resources.departamento_resource import departamento_bp
    from app.resources.certificado_resource import certificado_bp
    #from app.resources.tipo_especialidad_resource import tipo_especialidad_bp
    from app.resources.plan_resource import plan_bp
    from app.resources.cargo_resource import cargo_bp
    from app.resources.alumno_resource import alumno_bp

    # --- Registro con prefijo /sys ---
    app.register_blueprint(home_bp, url_prefix="/sys")
    app.register_blueprint(universidad_bp, url_prefix="/sys")
    app.register_blueprint(area_bp, url_prefix="/sys")
    app.register_blueprint(tipodocumento_bp, url_prefix="/sys")
    app.register_blueprint(tipodedicacion_bp, url_prefix="/sys")
    app.register_blueprint(categoriacargo_bp, url_prefix="/sys")
    app.register_blueprint(grupo_bp, url_prefix="/sys")
    app.register_blueprint(grado_bp, url_prefix="/sys")
    app.register_blueprint(departamento_bp, url_prefix="/sys")
    app.register_blueprint(certificado_bp, url_prefix="/sys")
    #app.register_blueprint(tipo_especialidad_bp, url_prefix="/sys")
    app.register_blueprint(plan_bp, url_prefix="/sys")
    app.register_blueprint(cargo_bp, url_prefix="/sys")
    app.register_blueprint(alumno_bp, url_prefix="/sys")

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}
    print(f"App created with context: {app_context}")
    return app
