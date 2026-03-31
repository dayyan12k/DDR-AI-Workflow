import fitz # PyMuPDF
import os

def process_pdf(pdf_path, output_image_dir="temp_images", prefix=""):
    if not os.path.exists(output_image_dir):
        os.makedirs(output_image_dir)
        
    doc = fitz.open(pdf_path)
    full_text = ""
    extracted_images = []
    
    # To avoid duplicate filenames when processing multiple PDFs
    base_name = prefix if prefix else os.path.splitext(os.path.basename(pdf_path))[0]
    
    # Some mock PDFs might generate images with odd names, we simply iterate text and images
    for page_num in range(len(doc)):
        page = doc[page_num]
        full_text += page.get_text() + "\n"
        
        # Get all images with their positioning info
        image_info = page.get_image_info(xrefs=True)
        
        for img_idx, info in enumerate(image_info):
            try:
                xref = info['xref']
                bbox = info['bbox'] # (x0, y0, x1, y1)
                
                # Expand bbox slightly to capture captions/labels
                context_bbox = (bbox[0] - 30, bbox[1] - 60, bbox[2] + 30, bbox[3] + 60)
                context_text = page.get_textbox(context_bbox).strip()
                
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                if image_ext not in ["jpg", "jpeg", "png"]:
                    image_ext = "jpg"
                    
                img_filename = f"{base_name}_page{page_num+1}_img{img_idx+1}.{image_ext}"
                img_filepath = os.path.join(output_image_dir, img_filename)
                
                with open(img_filepath, "wb") as f:
                    f.write(image_bytes)
                    
                extracted_images.append({
                    "filename": img_filename,
                    "filepath": img_filepath,
                    "page": page_num + 1,
                    "context": context_text # This is the "magic" metadata for the AI
                })
            except Exception as e:
                print(f"Warning: Could not extract image {img_idx} from page {page_num}: {e}")
            
    doc.close()
    return {
        "text": full_text,
        "images": extracted_images
    }
