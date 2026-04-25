from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import datetime

def create_report():
    doc = Document()
    
    # --- TITLE PAGE ---
    def add_centered_text(text, size=12, bold=False):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.size = Pt(size)
        run.bold = bold
        return p

    add_centered_text("Robotics and Drones Laboratory (22 MEC37N)", 14, True)
    add_centered_text("Project Report", 12, True)
    add_centered_text("On", 12)
    add_centered_text("Color Detection and pixel transition using OpenCV", 16, True)
    add_centered_text("By", 12)
    
    # Students Table
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Name of the student'
    hdr_cells[1].text = 'Roll Number'
    
    students = [
        ("Ronak Sarda", "160125737123"),
        ("Sai Bhardwaj reddy", "160124737124"),
        ("Abhinay", ""),
        ("Pranav", ""),
        ("Gauri Nandan", "")
    ]
    for name, roll in students:
        row_cells = table.add_row().cells
        row_cells[0].text = name
        row_cells[1].text = roll

    doc.add_paragraph("\n")
    add_centered_text("Under the Mentorship of", 12, True)
    add_centered_text("Dr. Kiran Kumar Amireddy", 12, True)
    add_centered_text("Assistant Professor", 12)
    
    add_centered_text("\nBranch: Department of Mechanical Engineering", 12)
    add_centered_text("\nSubmitted to", 12)
    add_centered_text("Department of Mechanical Engineering", 14, True)
    add_centered_text("CHAITANYA BHARATHI INSTITUTE OF TECHNOLOGY (A)", 14, True)
    add_centered_text("(Affiliated to Osmania University)", 12)
    add_centered_text("Gandipet, Hyderabad-500075", 12)
    add_centered_text("2024 - 2025", 12)
    
    doc.add_page_break()
    
    # --- CERTIFICATE ---
    add_centered_text("CERTIFICATE", 16, True)
    doc.add_paragraph("\nThis is to certify that the project entitled \"Color Detection and pixel transition using OpenCV\" by the following students has been carried out under my mentorship.")
    
    for i, (name, _) in enumerate(students, 1):
        doc.add_paragraph(f"{i}. {name}")
        
    doc.add_paragraph("\n\n\n\n")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run("Dr. Kiran Kumar Amireddy\nAssistant Professor")
    run.bold = True

    doc.add_page_break()
    
    # --- TOPICS ---
    sections = [
        ("1. Aim", "To develop an interactive Color Detection System using OpenCV that can precisely identify colors from images and perform smooth pixelated transitions between states using mathematical interpolation and color quantization."),
        ("2. Background and Motivation", "Color detection is a fundamental task in computer vision, especially for Robotics and Drones where real-time object tracking and environment mapping are required. This project is motivated by the need for accurate color categorization (mapping raw RGB values to human-readable names) and visualizing state transitions in a pixelated, compressed format."),
        ("3. Apparatus and Tools used", "Software Environment:\n- Python 3.10+\n- OpenCV (cv2): For image processing and UI.\n- Pandas: For color dataset management.\n- NumPy: For vectorized Euclidean distance calculations.\n- OS: Windows"),
        ("4. Detailed procedure", "1. Dataset Loading: Read 'colors.csv' containing 865 named colors.\n2. Interface: Create an OpenCV window with a mouse callback to track coordinates.\n3. Detection: Calculate Euclidean Distance between the pixel under mouse and all CSV entries.\n4. Shape Generation: Procedurally draw objects (Apple, Ball, Car, etc.) on a canvas.\n5. Pixelation: Use AREA interpolation to downsample and NEAREST to upsample.\n6. Morphing: Implement Linear Interpolation (LERP) using cv2.addWeighted to transition between images smoothly."),
        ("5. Hardware/Software Architecture", "The system follows a modular architecture:\n- Input Layer: Image file (pallete.jpg) or generated canvas.\n- Processing Layer: Euclidean distance matching and Quantization.\n- Visualization Layer: Smooth transition engine (25 steps per morph).\n- UI Layer: Real-time tooltip overlay."),
        ("6. Program/Code", "The code implements vectorized quantization for speed and procedural drawing functions to avoid external dependencies. It uses waitKey() to capture alphabet triggers (A-I) and the 'R' key for a smooth reset."),
        ("7. Output", "Pressing 'A' morphs the image into a pixelated Apple. Pressing 'C' morphs it into a Car. The 'R' key restores the original image through a 15-step smooth transition. The UI provides real-time RGB values and color names (e.g., 'Midnight Blue')."),
        ("8. Conclusions", "The project successfully demonstrates the power of OpenCV for interactive systems. By using vectorized NumPy operations, we achieved high-performance color matching across 865 entries. The smooth morphing logic provides a visually appealing and professional way to transition between image states."),
        ("9. References", "- OpenCV Documentation (docs.opencv.org)\n- Python-Docx API Documentation\n- Pandas Data Analysis Library")
    ]
    
    for title, content in sections:
        h = doc.add_heading(title, level=1)
        doc.add_paragraph(content)

    doc.save("Project_Report_ColorDetection.docx")
    print("Report generated: Project_Report_ColorDetection.docx")

if __name__ == "__main__":
    create_report()
