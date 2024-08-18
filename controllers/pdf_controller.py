import os
import PyPDF2
import re
from services.service_seamless import SeamlessTranslator
from services.service_functions.clean_output import clean_output

class PDFController:
    def __init__(self):
        self.translator = SeamlessTranslator()

    def count_paragraphs_in_pdf(self, pdf_path):
        paragraph_count = 0
        paragraphs = []
        
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            for page in reader.pages:
                text = page.extract_text()
                page_paragraphs = re.split(r'\n\s*\n', text)
                paragraphs.extend(page_paragraphs)
                paragraph_count += len(page_paragraphs)
        
        return paragraph_count, paragraphs

    def translate_pdf(self, pdf_path, src_lang, tgt_lang, start_paragraph=None, end_paragraph=None):
        try:
            if not os.path.exists(pdf_path):
                return {"status": "error", "message": "PDF file not found"}
            
            paragraph_count, paragraphs = self.count_paragraphs_in_pdf(pdf_path)
            
            if start_paragraph is not None and end_paragraph is not None:
                if start_paragraph < 1 or end_paragraph > paragraph_count or start_paragraph > end_paragraph:
                    return {"status": "error", "message": f"Invalid paragraph range. The PDF has {paragraph_count} paragraphs."}
                text_to_translate = "\n\n".join(paragraphs[start_paragraph-1:end_paragraph])
            else:
                text_to_translate = "\n\n".join(paragraphs)
            
            translated_text = self.translator.translate_text(text_to_translate, src_lang, tgt_lang)
            translated_text = clean_output(translated_text)
            return {
                "status": "success",
                "translated_text": translated_text,
                "paragraph_count": paragraph_count
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
