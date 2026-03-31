import google.generativeai as genai
import os
import json
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
_api_key = os.environ.get("GEMINI_API_KEY")
if _api_key:
    genai.configure(api_key=_api_key)

def generate_ddr_report(inspection_data, thermal_data):
    # Utilizing advanced Gemini 2.5 Flash model to avoid Free Tier Rate Limits
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = """
You are an expert technical inspector and AI data synthesizer. Your task is to generate a Detailed Diagnostic Report (DDR) by logically merging data from a Standard Inspection Report and a Thermal Report.

You must follow these instructions strictly:
1. Avoid duplicate points.
2. If information conflicts between the two reports (e.g. differing explanations), explicitly mention the conflict.
3. If information is missing for a required section, write "Not Available".
4. Use simple, client-friendly language and avoid unnecessary technical jargon.
5. You MUST include images in your output. You are provided with image files and their **Metadata (Filename, Page Number, and Contextual Text from the PDF)**. Use this metadata as your primary signal to match an image to an observation.
6. In the "area_wise_observations" section, whenever you write an observation, examine the provided images. Identify which images correspond to that observation based on the contextual text or page number, and inline the exact image filename inside brackets like so: `[IMAGE: {filename}]`.
7. If an image in the report is not clearly linked with the text, avoid making incorrect assumptions and instead safely mark it as "Image Not Available."
8. Do NOT invent facts or hallucinate image filenames that aren't provided.

You will output a STRICT JSON object answering the 7 required sections:
{
  "property_issue_summary": "High-level summary of the overall issues...",
  "area_wise_observations": [
     {
       "area": "name of area (e.g., Roof)",
       "observations": "detailed combined observation. [IMAGE: filename1.jpg]"
     }
  ],
  "probable_root_cause": "The likely root causes...",
  "severity_assessment": "Low/Medium/High with reasoning...",
  "recommended_actions": ["Action 1", "Action 2"],
  "additional_notes": "Any other notes...",
  "missing_or_unclear_information": "Any missing info, or 'Not Available'"
}

Below is the provided data:

=== INSPECTION REPORT TEXT ===
{inspection_text}

=== THERMAL REPORT TEXT ===
{thermal_text}

Additionally, images from these reports are provided in the current multimodal context. Each image is accompanied by its Filename, Page Number, and surrounding Contextual Text from the original document. Use your vision and this metadata together to place images accurately.
"""
    formatted_prompt = prompt.replace(
        "{inspection_text}", inspection_data["text"]
    ).replace(
        "{thermal_text}", thermal_data["text"]
    )
    
    parts = [formatted_prompt]
    
    for itm in inspection_data['images'] + thermal_data['images']:
        meta = f"Filename: {itm['filename']}, Page: {itm['page']}, Context: {itm.get('context', 'None')}"
        parts.append(meta)
        img = Image.open(itm['filepath'])
        parts.append(img)
            
    try:
        response = model.generate_content(
            parts,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        raise e
