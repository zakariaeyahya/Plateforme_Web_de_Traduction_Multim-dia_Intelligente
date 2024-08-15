from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from seamless_translator import SeamlessTranslator
import os
import tempfile
import logging

app = FastAPI()
translator = SeamlessTranslator()

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/translate_text/")
async def translate_text(input_text: str = Form(...), input_lang: str = Form(...), output_lang: str = Form(...)):
    try:
        logger.info(f"Demande de traduction de texte reçue: {input_lang} -> {output_lang}")
        translated_text = translator.translate_text(input_text, input_lang, output_lang)
        return {"translated_text": translated_text}
    except Exception as e:
        logger.error(f"Erreur lors de la traduction du texte: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate_pdf/")
async def translate_pdf(input_lang: str = Form(...), output_lang: str = Form(...), file: UploadFile = File(...)):
    logger.info(f"Demande de traduction de PDF reçue: {input_lang} -> {output_lang}")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        try:
            temp_pdf.write(await file.read())
            temp_pdf_path = temp_pdf.name
            
            translated_text = translator.translate_pdf(temp_pdf_path, input_lang, output_lang)
            return {"translated_text": translated_text}
        except Exception as e:
            logger.error(f"Erreur lors de la traduction du PDF: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            os.remove(temp_pdf_path)
            logger.info(f"Fichier PDF temporaire supprimé: {temp_pdf_path}")

@app.post("/translate_video/")
async def translate_video(input_lang: str = Form(...), output_lang: str = Form(...), ffmpeg_path: str = Form(...), file: UploadFile = File(...)):
    logger.info(f"Demande de traduction de vidéo reçue: {input_lang} -> {output_lang}")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        try:
            temp_video.write(await file.read())
            temp_video_path = temp_video.name
            
            transcription, translation = translator.transcribe_and_translate_video(temp_video_path, ffmpeg_path, input_lang, output_lang)
            
            if transcription and translation:
                return {"transcription": transcription, "translation": translation}
            else:
                raise HTTPException(status_code=500, detail="Erreur lors du traitement de la vidéo")
        except Exception as e:
            logger.error(f"Erreur lors de la traduction de la vidéo: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            os.remove(temp_video_path)
            logger.info(f"Fichier vidéo temporaire supprimé: {temp_video_path}")