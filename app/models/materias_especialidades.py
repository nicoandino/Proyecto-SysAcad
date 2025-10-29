from app import db

materias_especialidades = db.Table(
    "materias_especialidades",
    db.Column(
        "materia_id",
        db.Integer,
        db.ForeignKey("materias.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "especialidad_id",
        db.Integer,
        db.ForeignKey("especialidades.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
