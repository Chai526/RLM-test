import os
import shutil
import pymupdf as fitz  # PyMuPDF
from dotenv import load_dotenv

# --- CONFIGURATION ---
INPUT_DIR = "./pdfs"
PROCESSED_DIR = "./processed_pdfs"
STORAGE_FILE = "./knowledge_base.txt"

def ensure_dirs():
    """Ensure necessary directories exist."""
    for folder in [INPUT_DIR, PROCESSED_DIR]:
        if not os.path.exists(folder):
            os.makedirs(folder)

def extract_text_from_pdf(pdf_path):
    """Extracts text from a single PDF file."""
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

def main():
    ensure_dirs()
    
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.pdf')]
    
    if not files:
        print("No new PDFs found to process.")
        return

    print(f"Found {len(files)} new files. Starting ingestion...")

    with open(STORAGE_FILE, "a", encoding="utf-8") as f_out:
        for filename in files:
            input_path = os.path.join(INPUT_DIR, filename)
            dest_path = os.path.join(PROCESSED_DIR, filename)
            
            print(f"Processing: {filename}...")
            
            # 1. Extract
            content = extract_text_from_pdf(input_path)
            
            # 2. Store with metadata for context
            f_out.write(f"\n--- SOURCE: {filename} ---\n")
            f_out.write(content)
            f_out.write("\n--- END SOURCE ---\n")
            
            # 3. Move file to prevent duplication
            shutil.move(input_path, dest_path)
            print(f"✅ Successfully moved {filename} to processed folder.")

    print(f"\nIngestion complete. Knowledge base updated at: {STORAGE_FILE}")

if __name__ == "__main__":
    main()