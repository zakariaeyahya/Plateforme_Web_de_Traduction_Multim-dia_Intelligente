import streamlit as st
from seamless_translator import SeamlessTranslator
import os
import tempfile
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the translator
translator = SeamlessTranslator()

# Predefined FFmpeg path
FFMPEG_PATH = r"C:\Users\HP\anaconda3\pkgs\ffmpeg-4.3.1-ha925a31_0\Library\bin\ffmpeg.exe"

st.title("Document and Video Translator")

# Input options
input_type = st.selectbox("Choose input type", ["Text", "PDF", "Video"])

input_lang = st.selectbox("Source language", ["français", "anglais", "arabe", "darija"])
output_lang = st.selectbox("Target language", ["français", "anglais", "arabe", "darija"])

if input_type == "Text":
    input_text = st.text_area("Enter text to translate")

    if st.button("Translate Text"):
        try:
            logger.info(f"Début de la traduction de texte: {input_lang} -> {output_lang}")
            translated_text = translator.translate_text(input_text, input_lang, output_lang)
            st.text_area("Translated Text", translated_text)
            logger.info("Traduction de texte terminée avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de la traduction du texte: {e}")
            st.error(f"An error occurred: {e}")

elif input_type == "PDF":
    pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])

    if st.button("Translate PDF") and pdf_file:
        try:
            logger.info(f"Début de la traduction de PDF: {input_lang} -> {output_lang}")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(pdf_file.read())
                temp_pdf_path = temp_pdf.name
            
            translated_text = translator.translate_pdf(temp_pdf_path, input_lang, output_lang)
            st.text_area("Translated PDF Text", translated_text)
            logger.info("Traduction de PDF terminée avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de la traduction du PDF: {e}")
            st.error(f"An error occurred: {e}")
        finally:
            os.remove(temp_pdf_path)
            logger.info(f"Fichier PDF temporaire supprimé: {temp_pdf_path}")

elif input_type == "Video":
    video_file = st.file_uploader("Upload Video file", type=["mp4"])

    if st.button("Transcribe and Translate Video") and video_file:
        try:
            logger.info(f"Début de la transcription et traduction de vidéo: {input_lang} -> {output_lang}")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
                temp_video.write(video_file.read())
                temp_video_path = temp_video.name
            
            transcription, translation = translator.transcribe_and_translate_video(temp_video_path, FFMPEG_PATH, input_lang, output_lang)
            
            if transcription and translation:
                st.text_area("Transcription", transcription)
                st.text_area("Translation", translation)
                logger.info("Transcription et traduction de vidéo terminées avec succès")
            else:
                st.error("An error occurred during video processing.")
                logger.error("Échec de la transcription et traduction de vidéo")
        except Exception as e:
            logger.error(f"Erreur lors du traitement de la vidéo: {e}")
            st.error(f"An error occurred: {e}")
        finally:
            os.remove(temp_video_path)
            logger.info(f"Fichier vidéo temporaire supprimé: {temp_video_path}")
