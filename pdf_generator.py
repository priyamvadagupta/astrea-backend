from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import re

def clean_text_for_pdf(text):
    text = text.replace("**", "")
    text = text.replace("*", "")
    text = text.replace("#", "")
    text = text.replace("`", "")
    text = text.replace("“", "")
    text = text.replace("”", "")
    text = text.replace('"', "")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def generate_pdf(chart, ai_text, filename="astrology_report.pdf"):
    ai_text = clean_text_for_pdf(ai_text)

    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Astrea Vedic Astrology Report</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"<b>Ascendant:</b> {chart['ascendant']}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # story.append(Paragraph("<b>North Indian Birth Chart</b>", styles["Heading2"]))
    # story.append(Image(chart_image, width=330, height=330))
    # story.append(Spacer(1, 16))

    # Planet table
    story.append(Paragraph("<b>Planetary Positions</b>", styles["Heading2"]))

    planet_data = [["Planet", "Sign", "House", "Degree"]]
    for planet, details in chart["planets"].items():
        planet_data.append([
            planet,
            details["sign"],
            str(details["house"]),
            str(details["degree"])
        ])

    planet_table = Table(planet_data, colWidths=[90, 110, 70, 80])
    planet_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    story.append(planet_table)
    story.append(Spacer(1, 16))

    # House table
    story.append(Paragraph("<b>House Summary</b>", styles["Heading2"]))

    house_data = [["House", "Sign", "Planets"]]
    for house, details in chart["house_chart"].items():
        planets = ", ".join(details["planets"]) if details["planets"] else "-"
        house_data.append([
            str(house),
            details["sign"],
            planets
        ])

    house_table = Table(house_data, colWidths=[70, 120, 220])
    house_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    story.append(house_table)
    story.append(Spacer(1, 16))

    # AI interpretation
    story.append(Paragraph("<b>AI Interpretation With Reasoning</b>", styles["Heading2"]))

    for line in ai_text.split("\n"):
        if line.strip():
            story.append(Paragraph(line.strip(), styles["Normal"]))
            story.append(Spacer(1, 6))

    doc.build(story)
    return filename