import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image

def create_dummy_image(filename, color, text):
    img = Image.new('RGB', (400, 300), color=color)
    img.save(filename)

def create_inspection_report(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "Site Inspection Report")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "Date: Oct 26, 2023 | Inspector: John Doe")
    c.drawString(50, height - 130, "1. Roof Area Observations:")
    c.drawString(70, height - 150, "- Found severe water pooling near the HVAC unit.")
    c.drawString(70, height - 170, "- The membrane appears worn out but no visible tears yet.")
    
    c.drawString(50, height - 210, "2. Electrical Panel Basement:")
    c.drawString(70, height - 230, "- Main breaker box has loose wiring.")
    c.drawString(70, height - 250, "- Signs of oxidation on the copper lines.")
    
    # Create and add a generic image
    img_filename = "roof_crack.jpg"
    create_dummy_image(img_filename, (200, 200, 200), "Roof Crack")
    c.drawImage(img_filename, 50, height - 500, width=300, height=200)
    c.drawString(50, height - 520, "Fig 1: View of the roof near the HVAC unit.")
    
    c.save()
    if os.path.exists(img_filename):
        os.remove(img_filename)

def create_thermal_report(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "Thermal Imaging Report")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "Date: Oct 26, 2023 | Technician: Jane Smith")
    c.drawString(50, height - 130, "1. Roof Area Thermal Scan:")
    c.drawString(70, height - 150, "- Anomaly detected beneath the pooled water.")
    c.drawString(70, height - 170, "- Temperature delta of 4.5 C identified indicating trapped moisture.")
    
    # Create and add a generic thermal-like image
    thermal_filename = "thermal_roof.jpg"
    create_dummy_image(thermal_filename, (255, 50, 50), "Thermal Roof")
    c.drawImage(thermal_filename, 50, height - 400, width=300, height=200)
    c.drawString(50, height - 420, "Fig A: Thermal view showing cold spots near HVAC.")

    c.drawString(50, height - 460, "2. Electrical Panel Basement Thermal Scan:")
    c.drawString(70, height - 480, "- High temp detected on Breaker 4 (75 C).")
    c.drawString(70, height - 500, "- Potential overload or loose connection leading to overheating.")
    
    thermal_breaker_filename = "thermal_breaker.jpg"
    create_dummy_image(thermal_breaker_filename, (255, 150, 50), "Thermal Breaker")
    c.drawImage(thermal_breaker_filename, 50, height - 720, width=300, height=200)
    c.drawString(50, height - 740, "Fig B: IR scan of the main breaker box showing hotspot.")
    
    c.save()
    
    if os.path.exists(thermal_filename):
        os.remove(thermal_filename)
    if os.path.exists(thermal_breaker_filename):
        os.remove(thermal_breaker_filename)

if __name__ == "__main__":
    create_inspection_report("sample_inspection.pdf")
    create_thermal_report("sample_thermal.pdf")
    print("Generated mock reports: sample_inspection.pdf & sample_thermal.pdf")
