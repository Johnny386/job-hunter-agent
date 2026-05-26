from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from datetime import datetime
import os
import re

def clean_markdown(text: str) -> str:
    text = re.sub(r'#{1,6}\s*', '', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'•\s*--', '', text)
    text = re.sub(r'-{2,}', '', text)
    return text.strip()

def generate_pdf(content: str, content_type: str, company: str) -> dict:
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{content_type}_{company}_{timestamp}.pdf"
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(BASE_DIR, "output", filename)
        os.makedirs(os.path.join(BASE_DIR, "output"), exist_ok=True)

        content = clean_markdown(content)

        doc = SimpleDocTemplate(
            output_path, pagesize=A4,
            rightMargin=18*mm, leftMargin=18*mm,
            topMargin=15*mm, bottomMargin=15*mm
        )

        if content_type == "resume":
            story = build_resume(content)
        else:
            story = build_cover_letter(content)

        doc.build(story)
        return {"path": output_path, "error": None}

    except Exception as e:
        return {"path": None, "error": str(e)}


def build_resume(content: str):
    # Styles
    name_style = ParagraphStyle(
        "Name", fontSize=20, fontName="Helvetica-Bold",
        alignment=TA_CENTER, spaceAfter=3
    )
    contact_style = ParagraphStyle(
        "Contact", fontSize=9, fontName="Helvetica",
        alignment=TA_CENTER, textColor=colors.HexColor("#444444"),
        spaceAfter=8
    )
    section_style = ParagraphStyle(
        "Section", fontSize=10, fontName="Helvetica-Bold",
        spaceBefore=10, spaceAfter=2,
        textColor=colors.HexColor("#1a1a1a"),
        textTransform="uppercase"
    )
    job_title_style = ParagraphStyle(
        "JobTitle", fontSize=10, fontName="Helvetica-Bold",
        spaceBefore=6, spaceAfter=0
    )
    job_meta_style = ParagraphStyle(
        "JobMeta", fontSize=9, fontName="Helvetica-Oblique",
        textColor=colors.HexColor("#555555"), spaceAfter=3
    )
    body_style = ParagraphStyle(
        "Body", fontSize=9, fontName="Helvetica",
        leading=14, spaceAfter=2
    )
    bullet_style = ParagraphStyle(
        "Bullet", fontSize=9, fontName="Helvetica",
        leading=13, spaceAfter=2, leftIndent=10,
        firstLineIndent=0
    )

    story = []
    lines = content.strip().split("\n")
    i = 0

    # First line = name
    if lines:
        story.append(Paragraph(lines[0].strip(), name_style))
        i = 1

    # Second line = contact info
    if i < len(lines) and lines[i].strip():
        story.append(Paragraph(lines[i].strip(), contact_style))
        i += 1

    # Horizontal rule under header
    story.append(HRFlowable(width="100%", thickness=0.8,
                             color=colors.HexColor("#1a1a1a"), spaceAfter=6))

    # Rest of content
    while i < len(lines):
        line = lines[i].strip()
        i += 1

        if not line:
            story.append(Spacer(1, 3))
            continue

        # Section headers — ALL CAPS short lines
        if line.isupper() and len(line) < 40:
            story.append(Paragraph(line, section_style))
            story.append(HRFlowable(width="100%", thickness=0.5,
                                     color=colors.HexColor("#cccccc"), spaceAfter=3))
            continue

        # Bullet points
        if line.startswith("•") or line.startswith("-"):
            story.append(Paragraph(f"• {line[1:].strip()}", bullet_style))
            continue

        # Job title lines (followed by company/date line)
        if i < len(lines) and ("—" in lines[i] or "|" in lines[i] or
                                any(y in lines[i] for y in ["2022","2023","2024","2025","2026"])):
            story.append(Paragraph(line, job_title_style))
            continue

        # Company / date meta lines
        if "—" in line or (any(y in line for y in ["2022","2023","2024","2025","2026"])
                            and len(line) < 80):
            story.append(Paragraph(line, job_meta_style))
            continue

        # Default body
        story.append(Paragraph(line, body_style))

    return story


def build_cover_letter(content: str):
    body_style = ParagraphStyle(
        "Body", fontSize=11, fontName="Helvetica",
        leading=18, spaceAfter=12,
        textColor=colors.HexColor("#1a1a1a")
    )
    paragraphs = content.strip().split("\n\n")
    story = []
    story.append(Spacer(1, 10*mm))
    for p in paragraphs:
        if p.strip():
            story.append(Paragraph(p.strip().replace("\n", " "), body_style))
    return story