import os
from services.service_seamless import SeamlessTranslator

class PDFController:
    def __init__(self):
        self.translator = SeamlessTranslator()

    def translate_pdf(self, pdf_path, src_lang, tgt_lang):
        try:
            if not os.path.exists(pdf_path):
                return {"status": "error", "message": "PDF file not found"}
            
            translated_text = self.translator.translate_pdf(pdf_path, src_lang, tgt_lang)
            return {"status": "success", "translated_text": translated_text}
        except Exception as e:
            return {"status": "error", "message": str(e)}