"""
Herramienta de documentacion (NO es parte de los 10 ejercicios del taller):
convierte docs/explicacion.md a docs/explicacion.pdf.

Requiere `markdown` y `fpdf2` (ver docs/requirements-docs.txt); estas
librerias solo se usan para producir el PDF de entrega, no para resolver
ningun ejercicio.

Uso:
    python docs/generar_pdf.py
"""

import pathlib
import markdown
from fpdf import FPDF
from fpdf.fonts import FontFace, TextStyle

RAIZ = pathlib.Path(__file__).resolve().parent.parent
MD_PATH = RAIZ / "docs" / "explicacion.md"
PDF_PATH = RAIZ / "docs" / "explicacion.pdf"
# "Courier" y "Times" son nombres reservados de fuentes core de FPDF (no
# aceptan que se les asocie un archivo TTF propio), asi que la fuente
# monoespaciada para <code>/<pre> se registra con un nombre distinto.
FUENTES = {
    ("Arial", ""): "C:/Windows/Fonts/arial.ttf",
    ("Arial", "B"): "C:/Windows/Fonts/arialbd.ttf",
    ("Arial", "I"): "C:/Windows/Fonts/ariali.ttf",
    ("Arial", "BI"): "C:/Windows/Fonts/arialbi.ttf",
    ("CourierUnicode", ""): "C:/Windows/Fonts/cour.ttf",
    ("CourierUnicode", "B"): "C:/Windows/Fonts/courbd.ttf",
}


def construir_pdf():
    texto_md = MD_PATH.read_text(encoding="utf-8")
    html = markdown.markdown(texto_md, extensions=["fenced_code", "tables"])

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    for (familia, estilo), ruta in FUENTES.items():
        pdf.add_font(familia, estilo, ruta)
    pdf.set_font("Arial", size=11)
    pdf.write_html(
        html,
        tag_styles={
            "code": FontFace(family="CourierUnicode"),
            "pre": TextStyle(font_family="CourierUnicode", t_margin=4 + 7 / 30),
        },
    )
    pdf.output(str(PDF_PATH))
    print(f"PDF generado en: {PDF_PATH}")


if __name__ == "__main__":
    construir_pdf()
