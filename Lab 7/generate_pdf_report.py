import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#666666"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "LAB 7: Fuzzing for Input Validation Bugs")
            self.drawRightString(612 - 54, 755, "PES2UG24CS051 - Alakh Gupta")
            self.setStrokeColor(colors.HexColor("#dddddd"))
            self.setLineWidth(0.5)
            self.line(54, 747, 612 - 54, 747)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 30, page_text)
        self.drawString(54, 30, "Department of Computer Science and Engineering | PES University")
        self.setStrokeColor(colors.HexColor("#dddddd"))
        self.setLineWidth(0.5)
        self.line(54, 42, 612 - 54, 42)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1a202c"),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#4a5568"),
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=10,
        spaceAfter=4
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#2563eb"),
        spaceBefore=8,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor("#2d3748"),
        spaceAfter=4
    )

    caption_style = ParagraphStyle(
        'CaptionCustom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#4b5563"),
        alignment=1, # Center
        spaceAfter=6
    )

    story = []

    # Title & Header
    story.append(Paragraph("LAB 7: Fuzzing for Input Validation Bugs", title_style))
    story.append(Paragraph("Software Engineering Lab Report | Property-Based Testing with Hypothesis", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#1e3a8a"), spaceAfter=8))

    # Student metadata box
    meta_data = [
        [Paragraph("<b>Student Name:</b>", body_style), Paragraph("Alakh Gupta", body_style),
         Paragraph("<b>SRN:</b>", body_style), Paragraph("PES2UG24CS051", body_style)],
        [Paragraph("<b>Course:</b>", body_style), Paragraph("Software Engineering (SE)", body_style),
         Paragraph("<b>Repository:</b>", body_style), Paragraph("<a href='https://github.com/Alakhg1408/L6_L7_47_fuel_station.git' color='#2563eb'>L6_L7_47_fuel_station</a>", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[85, 165, 80, 174])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 6))

    # Objective
    story.append(Paragraph("1. Objective & Learning Outcomes", h1_style))
    story.append(Paragraph(
        "The objective of this lab is to explore <b>fuzz testing</b> as a dynamic security and quality assurance technique by identifying and hardening input validation bugs in a Python application using the <b>Hypothesis</b> property-based fuzzing library. Key outcomes include understanding automated edge-case generation, shrinking minimal failing inputs, and applying defensive programming techniques to prevent unhandled crashes.",
        body_style
    ))

    # Step 1
    story.append(Paragraph("2. Step 1: Installing Dependencies", h1_style))
    story.append(Paragraph(
        "The required testing libraries were installed using pip:<br/>"
        "• <code>pip install hypothesis</code><br/>"
        "• <code>pip install pytest</code>",
        body_style
    ))

    # Step 2
    story.append(Paragraph("3. Step 2: Running the Buggy Application", h1_style))
    story.append(Paragraph(
        "The application script under test implements a fuel station service with three functions: "
        "<code>parse_purchase(text)</code>, <code>volume_average(volumes_csv)</code>, and <code>payable_bill(text)</code>. "
        "The original buggy implementation assumes well-formed inputs and performs naive string splits and conversions without validation.",
        body_style
    ))
    
    img2_path = "/Users/alakhgupta/Documents/L6_L7_47_fuel_station/Lab 7/screenshots/step2_buggy_output.png"
    if os.path.exists(img2_path):
        img2 = Image(img2_path, width=490, height=160)
        story.append(img2)
        story.append(Paragraph("Figure 1: Screenshot of running the initial application with nominal valid inputs.", caption_style))

    story.append(PageBreak())

    # Step 3 & 4
    story.append(Paragraph("4. Step 3 & 4: Property-Based Fuzz Testing & Bug Discovery", h1_style))
    story.append(Paragraph(
        "In <code>test_processor.py</code> (and <code>test_fuel_station.py</code>), test properties were defined using the "
        "<code>@given(st.text() | st.none())</code> decorator from Hypothesis to verify that none of the functions crash on unexpected or malformed inputs.",
        body_style
    ))

    img4_path = "/Users/alakhgupta/Documents/L6_L7_47_fuel_station/Lab 7/screenshots/step4_failing_tests.png"
    if os.path.exists(img4_path):
        img4 = Image(img4_path, width=490, height=230)
        story.append(img4)
        story.append(Paragraph("Figure 2: Screenshot of pytest failures exposed by Hypothesis fuzzing on buggy code.", caption_style))

    story.append(Paragraph("<b>Analysis of Failing Test Cases Discovered by Hypothesis:</b>", h2_style))
    
    table_bugs = [
        [Paragraph("<b>Function</b>", body_style), Paragraph("<b>Falsifying Input</b>", body_style), Paragraph("<b>Exception / Bug Type</b>", body_style), Paragraph("<b>Root Cause</b>", body_style)],
        [Paragraph("<code>parse_purchase(text)</code>", body_style), Paragraph("<code>s = None</code><br/><code>s = ''</code><br/><code>s = ':'</code>", body_style), Paragraph("<code>AttributeError</code><br/><code>ValueError</code><br/><code>ValueError</code>", body_style), Paragraph("NoneType has no <code>split</code>; empty string has 1 item (expected 2); empty litres cannot convert to float.", body_style)],
        [Paragraph("<code>volume_average(csv)</code>", body_style), Paragraph("<code>s = None</code><br/><code>s = ''</code>", body_style), Paragraph("<code>AttributeError</code><br/><code>ValueError</code>", body_style), Paragraph("NoneType has no <code>split</code>; <code>int('')</code> fails on empty CSV elements.", body_style)],
        [Paragraph("<code>payable_bill(text)</code>", body_style), Paragraph("<code>s = None</code><br/><code>s = ''</code><br/><code>s = '|'</code>", body_style), Paragraph("<code>AttributeError</code><br/><code>ValueError</code><br/><code>ValueError</code>", body_style), Paragraph("NoneType has no <code>split</code>; splitting empty string lacks delimiter; empty bill cannot convert to float.", body_style)]
    ]
    t_bugs = Table(table_bugs, colWidths=[110, 80, 110, 204])
    t_bugs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_bugs)

    story.append(PageBreak())

    # Step 5
    story.append(Paragraph("5. Step 5: Defensive Hardening & Application Fixes", h1_style))
    story.append(Paragraph(
        "Defensive programming principles were applied across all three functions to handle edge cases gracefully:<br/>"
        "• <b>Type Validation:</b> Verified that incoming arguments are valid string instances using <code>isinstance(..., str)</code>, returning safe defaults when <code>None</code> or non-strings are passed.<br/>"
        "• <b>Structure & Length Checks:</b> Verified that delimiter splitting produces exactly two non-empty tokens before unpacking.<br/>"
        "• <b>Number Formatting & Boundary Checks:</b> Protected numeric parsing with <code>try...except (ValueError, OverflowError)</code> and checked against <code>math.isnan</code>, <code>math.isinf</code>, and negative values.<br/>"
        "• <b>Safe Fallbacks:</b> Returned <code>None</code> for invalid purchases, <code>0</code> for empty/invalid volume CSVs, and <code>0.0</code> for invalid bills.",
        body_style
    ))

    img5_path = "/Users/alakhgupta/Documents/L6_L7_47_fuel_station/Lab 7/screenshots/step5_fixed_output.png"
    if os.path.exists(img5_path):
        img5 = Image(img5_path, width=490, height=135)
        story.append(img5)
        story.append(Paragraph("Figure 3: Screenshot of running the hardened application script successfully.", caption_style))

    # Step 6
    story.append(Paragraph("6. Step 6: Re-Running Tests on Hardened Application", h1_style))
    story.append(Paragraph(
        "After hardening the application script, <code>pytest -v test_processor.py</code> was re-executed. "
        "Hypothesis generated hundreds of arbitrary Unicode strings, control characters, empty strings, and <code>None</code> values. "
        "All test cases passed cleanly with <b>zero crashes</b>.",
        body_style
    ))

    img6_path = "/Users/alakhgupta/Documents/L6_L7_47_fuel_station/Lab 7/screenshots/step6_passing_tests.png"
    if os.path.exists(img6_path):
        img6 = Image(img6_path, width=490, height=125)
        story.append(img6)
        story.append(Paragraph("Figure 4: Screenshot of pytest showing all Hypothesis property tests passing (100%).", caption_style))

    # Deliverables Summary
    story.append(Paragraph("7. Summary of Deliverables", h1_style))
    deliv_data = [
        [Paragraph("<b>Deliverable</b>", body_style), Paragraph("<b>Artifact Location</b>", body_style), Paragraph("<b>Status</b>", body_style)],
        [Paragraph("1. PDF Document with Screenshots", body_style), Paragraph("<code>Lab 7/PES2UG24CS051_LAB07.pdf</code>", body_style), Paragraph("Completed", body_style)],
        [Paragraph("2. Fixed Application Python Script", body_style), Paragraph("<code>Lab 7/fuel_station.py</code> & <code>processor.py</code>", body_style), Paragraph("Hardened & Verified", body_style)],
        [Paragraph("3. Updated Test Script", body_style), Paragraph("<code>Lab 7/test_fuel_station.py</code> & <code>test_processor.py</code>", body_style), Paragraph("All 3 Tests Passing", body_style)]
    ]
    t_deliv = Table(deliv_data, colWidths=[150, 240, 114])
    t_deliv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_deliv)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Built PDF: {filename}")

if __name__ == "__main__":
    out_pdf = "/Users/alakhgupta/Documents/L6_L7_47_fuel_station/Lab 7/PES2UG24CS051_LAB07.pdf"
    build_pdf(out_pdf)
    import shutil
    shutil.copyfile(out_pdf, "/Users/alakhgupta/Documents/L6_L7_47_fuel_station/Lab 7/PES2UG24CS051_Lab_7_report.pdf")
    print("PDF generated successfully.")
