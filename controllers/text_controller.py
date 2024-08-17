from services.service_seamless import SeamlessTranslator

class TextController:
    def __init__(self):
        self.translator = SeamlessTranslator()

    def translate_text(self, text, src_lang, tgt_lang):
        try:
            translated_text = self.translator.translate_text(text, src_lang, tgt_lang)
            translated_text=clean_output(translated_text)
            return {"status": "success", "translated_text": translated_text}
        except Exception as e:
            return {"status": "error", "message": str(e)}
