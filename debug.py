from pdf_processor import process_pdf
from ai_analyzer import generate_ddr_report
print("Extracting...")
ins = process_pdf("sample_inspection.pdf", "img_dir")
thm = process_pdf("sample_thermal.pdf", "img_dir")
print("Images extracted:", [img.get('filename') for img in ins['images']], [img.get('filename') for img in thm['images']])
print("Calling AI Analyzer...")
try:
    res = generate_ddr_report(ins, thm)
    print("Success:", res)
except Exception as e:
    import traceback
    traceback.print_exc()
