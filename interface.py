import streamlit as st
import tempfile
import os
from controllers.text_controller import TextController
from controllers.pdf_controller import PDFController
from controllers.video_controller import VideoController
from controllers.audio_controller import AudioController
from services.service_functions import clean_output
# Initialisation des contrôleurs
text_controller = TextController()
pdf_controller = PDFController()
video_controller = VideoController(ffmpeg_path=r"C:\Users\HP\anaconda3\pkgs\ffmpeg-4.3.1-ha925a31_0\Library\bin\ffmpeg.exe")
audio_controller = AudioController(ffmpeg_path=r"C:\Users\HP\anaconda3\pkgs\ffmpeg-4.3.1-ha925a31_0\Library\bin\ffmpeg.exe")

st.title("Document, Video, and Audio Translator")

# Input options
input_type = st.selectbox("Choose input type", ["Text", "PDF", "Video", "Audio"])

input_lang = st.selectbox("Source language", ["français", "anglais", "arabe", "darija"])
output_lang = st.selectbox("Target language", ["français", "anglais", "arabe", "darija"])

if input_type == "Text":
    input_text = st.text_area("Enter text to translate")

    if st.button("Translate Text"):
        with st.spinner("Translating..."):
            result = text_controller.translate_text(input_text, input_lang, output_lang)
            if result["status"] == "success":
                st.text_area("Translated Text", result["translated_text"])
            else:
                st.error(f"An error occurred: {result['message']}")

elif input_type == "PDF":
    pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])

    if pdf_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(pdf_file.read())
            temp_pdf_path = temp_pdf.name
        
        try:
            paragraph_count, _ = pdf_controller.count_paragraphs_in_pdf(temp_pdf_path)
            st.write(f"Le PDF contient {paragraph_count} paragraphes.")
            
            translate_option = st.radio("Choisissez une option de traduction :", 
                                        ("Tout le PDF", "Une plage de paragraphes"))
            
            if translate_option == "Une plage de paragraphes":
                col1, col2 = st.columns(2)
                with col1:
                    start_paragraph = st.number_input("Du paragraphe :", 
                                                      min_value=1, max_value=paragraph_count, value=1)
                with col2:
                    end_paragraph = st.number_input("Au paragraphe :", 
                                                    min_value=start_paragraph, max_value=paragraph_count, value=min(start_paragraph+2, paragraph_count))
            else:
                start_paragraph = None
                end_paragraph = None

            if st.button("Traduire PDF"):
                with st.spinner("Traduction en cours..."):
                    result = pdf_controller.translate_pdf(temp_pdf_path, input_lang, output_lang, start_paragraph, end_paragraph)
                    if result["status"] == "success":
                        st.text_area("Texte traduit", result["translated_text"])
                    else:
                        st.error(f"Une erreur s'est produite : {result['message']}")
        finally:
            os.remove(temp_pdf_path)

elif input_type == "Video":
    video_file = st.file_uploader("Upload Video file", type=["mp4"])

    if st.button("Transcribe and Translate Video") and video_file:
        with st.spinner("Processing video..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
                temp_video.write(video_file.read())
                temp_video_path = temp_video.name
            
            try:
                result = video_controller.transcribe_and_translate_video(temp_video_path, input_lang, output_lang)
                if result["status"] == "success":
                    st.text_area("Transcription", result["transcription"])
                    st.text_area("Translation", result["translation"])
                else:
                    st.error(f"An error occurred: {result['message']}")
            finally:
                os.remove(temp_video_path)

elif input_type == "Audio":
    audio_file = st.file_uploader("Upload Audio file", type=["mp3", "opus", "wav"])
    audio_type = st.selectbox("Select audio type", ["mp3", "opus", "wav"])

    if audio_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.' + audio_type) as temp_audio:
            temp_audio.write(audio_file.read())
            temp_audio_path = temp_audio.name
        
        try:
            duration = audio_controller.get_audio_duration(temp_audio_path)
            st.write(f"La durée de l'audio est de {duration} secondes.")
            
            translate_option = st.radio("Choisissez une option de traduction :", 
                                        ("Tout l'audio", "Une plage de temps spécifique"))
            
            if translate_option == "Une plage de temps spécifique":
                col1, col2 = st.columns(2)
                with col1:
                    start_second = st.number_input("De la seconde :", 
                                                   min_value=0, max_value=duration-1, value=0)
                with col2:
                    end_second = st.number_input("À la seconde :", 
                                                 min_value=start_second+1, max_value=duration, value=min(start_second+10, duration))
            else:
                start_second = None
                end_second = None

            if st.button("Transcrire et Traduire Audio"):
                with st.spinner("Traitement audio en cours..."):
                    output_csv = tempfile.NamedTemporaryFile(delete=False, suffix=".csv").name
                    result = audio_controller.process_audio(temp_audio_path, input_lang, output_lang, output_csv, audio_type, start_second, end_second)
                    if result["status"] == "success":
                        st.text_area("Transcription", result["transcription"])
                        st.text_area("Traduction", result["translation"])
                        st.download_button(
                            label="Télécharger CSV",
                            data=open(output_csv, 'rb'),
                            file_name="audio_processing_results.csv",
                            mime="text/csv"
                        )
                    else:
                        st.error(f"Une erreur s'est produite : {result['message']}")
        finally:
            os.remove(temp_audio_path)
            if 'output_csv' in locals() and os.path.exists(output_csv):
                os.remove(output_csv)
