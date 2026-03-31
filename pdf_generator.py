import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch

def create_ddr_pdf(report_json, img_dir, output_pdf_path):
    doc = SimpleDocTemplate(output_pdf_path, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    
    title_style = styles['Heading1']
    title_style.alignment = 1 # Center
    
    heading2 = styles['Heading2']
    heading2.textColor = HexColor('#1f497d')
    heading2.spaceBefore = 15
    heading2.spaceAfter = 5
    
    normal = styles['Normal']
    normal.spaceAfter = 8
    normal.leading = 14
    
    bullet = ParagraphStyle('Bullet', parent=normal, leftIndent=20, bulletIndent=10)
    
    story = []
    
    story.append(Paragraph("Detailed Diagnostic Report (DDR)", title_style))
    story.append(Spacer(1, 0.25 * inch))
    
    def add_section(title, text):
        story.append(Paragraph(title, heading2))
        parts = re.split(r'(\[IMAGE:[^\]]+\])', str(text))
        for pt in parts:
            if pt.startswith("[IMAGE:") and pt.endswith("]"):
                filename = pt.replace("[IMAGE:", "").replace("]", "").strip()
                filepath = os.path.join(img_dir, filename)
                if os.path.exists(filepath):
                    story.append(Spacer(1, 0.05 * inch))
                    try:
                        img = RLImage(filepath, width=4*inch, height=2.5*inch, preserveAspectRatio=True)
                        story.append(img)
                    except:
                        pass
                    story.append(Spacer(1, 0.05 * inch))
                else:
                    story.append(Paragraph(f"<i>[Image Not Available: {filename}]</i>", normal))
            else:
                if pt.strip():
                    story.append(Paragraph(pt.replace('\n', '<br/>'), normal))
    
    # 1
    add_section("1. Property Issue Summary", report_json.get("property_issue_summary", "Not Available"))
    
    # 2
    story.append(Paragraph("2. Area-wise Observations", heading2))
    for area_obs in report_json.get("area_wise_observations", []):
        story.append(Paragraph(f"<b>{area_obs.get('area', 'Area')}</b>", normal))
        text = area_obs.get("observations", "")
        parts = re.split(r'(\[IMAGE:[^\]]+\])', text)
        for pt in parts:
            if pt.startswith("[IMAGE:") and pt.endswith("]"):
                filename = pt.replace("[IMAGE:", "").replace("]", "").strip()
                filepath = os.path.join(img_dir, filename)
                if os.path.exists(filepath):
                    try:
                        img = RLImage(filepath, width=4*inch, height=2.5*inch, preserveAspectRatio=True)
                        story.append(img)
                    except:
                        pass
            else:
                if pt.strip():
                    story.append(Paragraph(pt.replace('\n', '<br/>'), normal))

    # 3, 4
    add_section("3. Probable Root Cause", report_json.get("probable_root_cause", "Not Available"))
    add_section("4. Severity Assessment", report_json.get("severity_assessment", "Not Available"))

    # 5
    story.append(Paragraph("5. Recommended Actions", heading2))
    for act in report_json.get("recommended_actions", []):
        story.append(Paragraph(f"• {act}", bullet))

    # 6, 7
    add_section("6. Additional Notes", report_json.get("additional_notes", "Not Available"))
    add_section("7. Missing or Unclear Information", report_json.get("missing_or_unclear_information", "Not Available"))
    
    doc.build(story)
    return output_pdf_path
