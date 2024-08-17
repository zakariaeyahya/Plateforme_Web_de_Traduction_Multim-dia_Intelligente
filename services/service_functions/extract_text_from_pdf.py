import os
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    if not os.path.isfile(pdf_path):
        return ""
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            text = "\n".join(page.extract_text() for page in reader.pages)
            return text
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte du PDF: {e}")
        return ""