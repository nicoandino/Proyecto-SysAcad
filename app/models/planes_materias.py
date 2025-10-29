from app import db

planes_materias = db.Table(
    "planes_materias",
    db.Column(
        "plan_id",
        db.Integer,
        db.ForeignKey("planes.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "materia_id",
        db.Integer,
        db.ForeignKey("materias.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
