from .extract_text_from_pdf import extract_text_from_pdf

def translate_pdf(pdf_path, src_lang, tgt_lang, translate_text_func):
    text = extract_text_from_pdf(pdf_path)
    if text:
        translated_text = translate_text_func(text, src_lang, tgt_lang)
        return translated_text
    else:
        return ""