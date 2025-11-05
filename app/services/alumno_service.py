# app/services/alumno_service.py
from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Optional, Tuple
from flask import current_app
from docxtpl import DocxTemplate
import jinja2
from datetime import date
import pdfkit
from flask import render_template

from app import db
from app.models.alumno import Alumno
from app.repositories import AlumnoRepository


class AlumnoService:
    """
    Service de alumnos + generación de certificado en DOCX.
    - DRY: una única función privada arma el contexto del certificado.
    - KISS: paths claros, helpers chicos y puros.
    - YAGNI: sólo lo necesario para el certificado actual.
    """

    # ---------- CRUD simples apoyados en el repositorio ----------
    @staticmethod
    def crear(alumno: Alumno) -> None:
        AlumnoRepository.crear(alumno)

    @staticmethod
    def buscar_por_id(id: int) -> Optional[Alumno]:
        return AlumnoRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[Alumno]:
        return AlumnoRepository.buscar_todos()

    @staticmethod
    def actualizar(id: int, alumno: Alumno) -> Optional[Alumno]:
        existente = AlumnoRepository.buscar_por_id(id)
        if not existente:
            return None

        # Campos editables (evitamos sobrescribir relaciones sin querer)
        existente.nombre = alumno.nombre
        existente.apellido = alumno.apellido
        existente.nro_documento = alumno.nro_documento
        existente.tipo_documento = alumno.tipo_documento
        existente.fecha_nacimiento = alumno.fecha_nacimiento
        existente.sexo = alumno.sexo
        existente.nro_legajo = alumno.nro_legajo
        existente.fecha_ingreso = alumno.fecha_ingreso

        db.session.commit()
        return existente


    @staticmethod
    def borrar_por_id(id: int) -> bool:
        alumno = AlumnoRepository.borrar_por_id(id)
        return alumno is not None
    # ---------- Certificado DOCX ----------
    @staticmethod
    def generar_certificado_alumno_regular_docx(alumno_id: int) -> Optional[Tuple[BytesIO, str]]:
        """
        Genera el certificado de alumno regular en DOCX desde la plantilla:
        app/templates/certificado/certificado_plantilla.docx

        Retorna: (buffer_docx, nombre_archivo) o None si no existe el alumno.
        """
        alumno = AlumnoRepository.buscar_por_id(alumno_id)
        if not alumno:
            return None

        ctx = AlumnoService._contexto_certificado(alumno)
        plantilla = AlumnoService._ruta_plantilla()

        # FIX: validar existencia de la plantilla con log claro
        if not plantilla.exists():
            raise FileNotFoundError(f"No se encontró la plantilla DOCX en: {plantilla}")

        # Render con un entorno Jinja explícito (permite extender filtros si hiciera falta)
        jinja_env = jinja2.Environment(autoescape=True)

        tpl = DocxTemplate(str(plantilla))
        tpl.render(ctx, jinja_env)

        # Guardamos directo al buffer (sin archivos temporales)
        buffer = BytesIO()
        tpl.save(buffer)
        buffer.seek(0)

        filename = f"certificado_{ctx['alumno']['nro_legajo']}.docx"
        return buffer, filename

    # ---------- Helpers internos ----------
    @staticmethod
    def _ruta_plantilla() -> Path:
        # Evitamos errores con separadores de OS y mantenemos la ruta relativa al app.root_path
        return Path(current_app.root_path) / "templates" / "certificado" / "certificado_plantilla.docx"

    @staticmethod
    def _fecha_larga_es(d: date) -> str:
        # Sin depender de locale del sistema
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        return f"{d.day} de {meses[d.month - 1]} de {d.year}"

    @staticmethod
    def _tipo_doc_sigla_safe(alumno: Alumno) -> str:
        # Soporta tanto campo plano como relación a TipoDocumento(sigla)
        return (
            getattr(alumno, "tipo_documento_sigla", None)
            or getattr(getattr(alumno, "tipo_documento", None), "sigla", None)
            or getattr(alumno, "tipo_documento", "")  # FIX: si es string plano, úsalo
            or ""
        )
    @staticmethod
    def _contexto_certificado(alumno: Alumno) -> dict:
        esp = getattr(alumno, "especialidad", None)
        fac = getattr(esp, "facultad", None) if esp else None
        uni = getattr(fac, "universidad", None) if fac else None

        esp_nombre = getattr(esp, "nombre", "")
        fac_nombre = getattr(fac, "nombre", "")
        uni_nombre = getattr(uni, "nombre", "")

        tipo_doc_sigla = (
            getattr(getattr(alumno, "tipo_documento", None), "sigla", None)
            or getattr(alumno, "tipo_documento_sigla", "")
            or ""
        )

        nro_doc_val = str(getattr(alumno, "nro_documento", "") or "")

        return {
            "alumno": {
                "apellido": alumno.apellido or "",
                "nombre": alumno.nombre or "",
                "tipo_documento": {"sigla": tipo_doc_sigla},
                "nrodocumento": nro_doc_val,
                "nro_legajo": str(alumno.nro_legajo or ""),
                # ✅ Nueva línea
                "fecha_ingreso": alumno.fecha_ingreso.strftime("%d/%m/%Y") if alumno.fecha_ingreso else "",
            },
            "especialidad": {"nombre": esp_nombre},
            "facultad": {"nombre": fac_nombre},
            "universidad": {"nombre": uni_nombre},
            "fecha": AlumnoService._fecha_larga_es(date.today()),
        }

    @staticmethod
    def generar_certificado_alumno_regular_pdf(alumno_id: int):
        alumno = AlumnoRepository.buscar_por_id(alumno_id)
        if not alumno:
            return None

        ctx = AlumnoService._contexto_certificado(alumno)
        html_string = render_template("certificado/certificado_pdf.html", **ctx)

        # Ruta al ejecutable wkhtmltopdf
        config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
        pdf_bytes = pdfkit.from_string(html_string, False, configuration=config)

        buffer = BytesIO(pdf_bytes)
        filename = f"certificado_{ctx['alumno']['nro_legajo']}.pdf"
        return buffer, filename


    @staticmethod
    def serializar_alumno(alumno) -> dict:
        return {
            "nro_legajo": alumno.nro_legajo,
            "apellido": alumno.apellido,
            "nombre": alumno.nombre,
            "tipo_documento": getattr(alumno.tipo_documento, "sigla", alumno.tipo_documento),
            "nro_documento": alumno.nro_documento,
            "facultad": getattr(alumno.facultad, "nombre", ""),
            "especialidad": getattr(alumno.especialidad, "nombre", ""),
            "pais": getattr(alumno.pais, "nombre", ""),
            "fecha_ingreso": alumno.fecha_ingreso.strftime("%d/%m/%Y"),
        }

    @staticmethod
    def generar_ficha_alumno_pdf(alumno_id: int):
        alumno = AlumnoRepository.buscar_por_id(alumno_id)
        if not alumno:
            return None

        # ✅ usar el mismo contexto que el certificado
        ctx = AlumnoService._contexto_certificado(alumno)

        html = render_template(
            "fichaalumno/ficha_alumno.html",
            **ctx  # ✅ importante: descomponer el diccionario para pasar todas las claves
        )

        config = pdfkit.configuration(
            wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        )
        options = {"encoding": "UTF-8", "quiet": ""}

        pdf_bytes = pdfkit.from_string(html, False, configuration=config, options=options)
        buffer = BytesIO(pdf_bytes)
        filename = f"ficha_alumno_{ctx['alumno']['nro_legajo']}.pdf"
        return buffer, filename
