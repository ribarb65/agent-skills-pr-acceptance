"""Renders the proposal .docx to PDF with the same layout (Times 12 pt, Letter, 1-inch margins).

Used because no Word/LibreOffice is available for a native export.
Usage: python report/docx_to_pdf.py report/Project_Proposal.docx report/Project_Proposal.pdf
"""
import sys
from xml.sax.saxutils import escape

from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate

src = sys.argv[1] if len(sys.argv) > 1 else "report/Project_Proposal.docx"
out = sys.argv[2] if len(sys.argv) > 2 else "report/Project_Proposal.pdf"
d = Document(src)
base = ParagraphStyle("body", fontName="Times-Roman", fontSize=12, leading=14, spaceAfter=12)
story = []
for p in d.paragraphs:
    html, size = "", 12
    for r in p.runs:
        t = escape(r.text)
        if r.underline:
            t = f"<u>{t}</u>"
        if r.bold:
            t = f"<b>{t}</b>"
        html += t
        if r.font.size:
            size = r.font.size.pt
    story.append(Paragraph(html, ParagraphStyle("p", parent=base, fontSize=size, leading=size * 1.17)))

cp = d.core_properties
doc = SimpleDocTemplate(out, pagesize=letter, leftMargin=inch, rightMargin=inch, topMargin=inch,
                        bottomMargin=inch, title=cp.title, author=cp.author, creator=cp.author)
doc.build(story)
print("wrote", out)
