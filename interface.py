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

    if st.button("Translate PDF") and pdf_file:
        with st.spinner("Translating PDF..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(pdf_file.read())
                temp_pdf_path = temp_pdf.name
            
            try:
                result = pdf_controller.translate_pdf(temp_pdf_path, input_lang, output_lang)
                if result["status"] == "success":
                    st.text_area("Translated PDF Text", result["translated_text"])
                else:
                    st.error(f"An error occurred: {result['message']}")
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

    if st.button("Transcribe and Translate Audio") and audio_file:
        with st.spinner("Processing audio..."):
            file_extension = '.' + audio_type
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_audio:
                temp_audio.write(audio_file.read())
                temp_audio_path = temp_audio.name
            
            output_csv = tempfile.NamedTemporaryFile(delete=False, suffix=".csv").name
            
            try:
                result = audio_controller.process_audio(temp_audio_path, input_lang, output_lang, output_csv, audio_type)
                if result["status"] == "success":
                    st.text_area("Transcription", result["transcription"])
                    st.text_area("Translation", result["translation"])
                    st.download_button(
                        label="Download CSV",
                        data=open(output_csv, 'rb'),
                        file_name="audio_processing_results.csv",
                        mime="text/csv"
                    )
                else:
                    st.error(f"An error occurred: {result['message']}")
            finally:
                os.remove(temp_audio_path)
                os.remove(output_csv)
