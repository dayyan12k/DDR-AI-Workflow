import streamlit as st
import os
from pdf_processor import process_pdf
from ai_analyzer import generate_ddr_report
import tempfile
import re

st.set_page_config(page_title="DDR AI Generator", layout="wide")

st.title("Applied AI Builder: DDR Report Generation")
st.markdown("Upload standard inspection and thermal reports to generate a unified Detailed Diagnostic Report (DDR).")

col1, col2 = st.columns(2)
with col1:
    ins_file = st.file_uploader("Upload Inspection Report (PDF)", type=["pdf"])
with col2:
    thm_file = st.file_uploader("Upload Thermal Report (PDF)", type=["pdf"])

if st.button("Generate DDR Report", type="primary"):
    if ins_file and thm_file:
        with st.spinner("Processing Documents & Analyzing via Gemini..."):
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f_ins:
                f_ins.write(ins_file.getbuffer())
                ins_path = f_ins.name
                
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f_thm:
                f_thm.write(thm_file.getbuffer())
                thm_path = f_thm.name
                
            img_dir = os.path.join(tempfile.gettempdir(), "ddr_app_images")
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)
            
            # Process PDFs
            st.info("Extracting Text & Images from PDFs...")
            ins_data = process_pdf(ins_path, output_image_dir=img_dir, prefix="inspection_doc")
            thm_data = process_pdf(thm_path, output_image_dir=img_dir, prefix="thermal_doc")
            
            # AI generation
            st.info("Synthesizing Report with Gemini API...")
            report_json = generate_ddr_report(ins_data, thm_data)
            
            # Display report
            if report_json:
                st.success("Report Generated Successfully!")
                
                # Create the PDF in background
                from pdf_generator import create_ddr_pdf
                pdf_path = os.path.join(tempfile.gettempdir(), "final_ddr_report.pdf")
                create_ddr_pdf(report_json, img_dir, pdf_path)
                
                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()
                    
                st.download_button(
                    label="📄 Download DDR as PDF Document",
                    data=pdf_bytes,
                    file_name="DDR_Report.pdf",
                    mime="application/pdf",
                    type="primary"
                )
                
                def render_text_with_images(text):
                    parts = re.split(r'(\[IMAGE:[^\]]+\])', text)
                    for pt in parts:
                        if pt.startswith("[IMAGE:") and pt.endswith("]"):
                            filename = pt.replace("[IMAGE:", "").replace("]", "").strip()
                            filepath = os.path.join(img_dir, filename)
                            if os.path.exists(filepath):
                                st.image(filepath, caption=filename, width=400)
                            else:
                                st.warning(f"Image Not Available: {filename}")
                        else:
                            st.write(pt)

                st.divider()
                st.header("Detailed Diagnostic Report (DDR)")
                
                st.subheader("1. Property Issue Summary")
                st.write(report_json.get("property_issue_summary", "Not Available"))
                
                st.subheader("2. Area-wise Observations")
                for area_obs in report_json.get("area_wise_observations", []):
                    st.markdown(f"**{area_obs.get('area', 'Area')}**")
                    render_text_with_images(area_obs.get("observations", ""))
                    
                st.subheader("3. Probable Root Cause")
                st.write(report_json.get("probable_root_cause", "Not Available"))
                
                st.subheader("4. Severity Assessment")
                st.write(report_json.get("severity_assessment", "Not Available"))
                
                st.subheader("5. Recommended Actions")
                for act in report_json.get("recommended_actions", []):
                    st.write(f"- {act}")
                    
                st.subheader("6. Additional Notes")
                st.write(report_json.get("additional_notes", "Not Available"))
                
                st.subheader("7. Missing or Unclear Information")
                st.write(report_json.get("missing_or_unclear_information", "Not Available"))
                
            else:
                st.error("Failed to generate report. Check API keys and logs.")
            
    else:
        st.warning("Please upload both documents to proceed.")
