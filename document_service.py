import re
from pathlib import Path

def sanitize_text(text):
    if not text:
        return ""
    return str(text).strip()

def export_filename(doc_type, ext="txt"):
    safe = re.sub(r'[^a-zA-Z0-9]', '_', doc_type)
    return f"{safe}.{ext}"

def format_txt(text):
    return sanitize_text(text).encode("utf-8")

def format_docx(text, doc_type=""):
    from docx import Document
    doc = Document()
    doc.add_paragraph(sanitize_text(text))
    return doc

def format_pdf(text):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, sanitize_text(text))
    return pdf

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "assets" / "legal_ease_logo.png"
