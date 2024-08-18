from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import tempfile
import logging
from controllers.text_controller import TextController
from controllers.pdf_controller import PDFController
from controllers.video_controller import VideoController
from controllers.audio_controller import AudioController

app = FastAPI()

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation des contrôleurs
text_controller = TextController()
pdf_controller = PDFController()
video_controller = VideoController(ffmpeg_path="chemin/vers/ffmpeg")
audio_controller = AudioController(ffmpeg_path="chemin/vers/ffmpeg")

@app.post("/translate_text/")
async def translate_text(input_text: str = Form(...), input_lang: str = Form(...), output_lang: str = Form(...)):
    logger.info(f"Demande de traduction de texte reçue: {input_lang} -> {output_lang}")
    result = text_controller.translate_text(input_text, input_lang, output_lang)
    if result["status"] == "success":
        return JSONResponse(content=result, status_code=200)
    else:
        raise HTTPException(status_code=500, detail=result["message"])

@app.post("/translate_pdf/")
async def translate_pdf(
    input_lang: str = Form(...),
    output_lang: str = Form(...),
    start_paragraph: int = Form(None),
    end_paragraph: int = Form(None),
    file: UploadFile = File(...)
):
    logger.info(f"Demande de traduction de PDF reçue: {input_lang} -> {output_lang}")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(await file.read())
        temp_pdf_path = temp_pdf.name
    
    try:
        result = pdf_controller.translate_pdf(temp_pdf_path, input_lang, output_lang, start_paragraph, end_paragraph)
        if result["status"] == "success":
            return JSONResponse(content=result, status_code=200)
        else:
            raise HTTPException(status_code=500, detail=result["message"])
    finally:
        os.remove(temp_pdf_path)
        logger.info(f"Fichier PDF temporaire supprimé: {temp_pdf_path}")

@app.post("/translate_video/")
async def translate_video(input_lang: str = Form(...), output_lang: str = Form(...), file: UploadFile = File(...)):
    logger.info(f"Demande de traduction de vidéo reçue: {input_lang} -> {output_lang}")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(await file.read())
        temp_video_path = temp_video.name
    
    try:
        result = video_controller.transcribe_and_translate_video(temp_video_path, input_lang, output_lang)
        if result["status"] == "success":
            return JSONResponse(content=result, status_code=200)
        else:
            raise HTTPException(status_code=500, detail=result["message"])
    finally:
        os.remove(temp_video_path)
        logger.info(f"Fichier vidéo temporaire supprimé: {temp_video_path}")

@app.post("/process_audio/")
async def process_audio(
    input_lang: str = Form(...),
    output_lang: str = Form(...),
    audio_type: str = Form(...),
    start_second: int = Form(None),
    end_second: int = Form(None),
    file: UploadFile = File(...)
):
    logger.info(f"Demande de traitement audio reçue: {input_lang} -> {output_lang}, Type: {audio_type}")
    if audio_type not in ['mp3', 'opus', 'wav']:
        raise HTTPException(status_code=400, detail="Type audio non supporté. Utilisez 'mp3', 'opus', ou 'wav'.")
    
    file_extension = '.' + audio_type
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_audio:
        temp_audio.write(await file.read())
        temp_audio_path = temp_audio.name
    
    output_csv = tempfile.NamedTemporaryFile(delete=False, suffix=".csv").name
    
    try:
        result = audio_controller.process_audio(temp_audio_path, input_lang, output_lang, output_csv, audio_type, start_second, end_second)
        if result["status"] == "success":
            return JSONResponse(content=result, status_code=200)
        else:
            raise HTTPException(status_code=500, detail=result["message"])
    finally:
        os.remove(temp_audio_path)
        os.remove(output_csv)
        logger.info(f"Fichiers temporaires supprimés: {temp_audio_path}, {output_csv}")
