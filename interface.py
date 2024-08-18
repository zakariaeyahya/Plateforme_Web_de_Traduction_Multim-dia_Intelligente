import streamlit as st
import tempfile
import os
from controllers.text_controller import TextController
from controllers.pdf_controller import PDFController
from controllers.video_controller import VideoController
from controllers.audio_controller import AudioController
from services.service_functions import clean_output
from services.service_functions.text_file_functions import read_text_file
from controllers.text_file_controller import TextFileController
# Initialisation des contrôleurs
text_controller = TextController()
pdf_controller = PDFController()
text_file_controller=TextFileController()
video_controller = VideoController(ffmpeg_path=r"C:\Users\HP\anaconda3\pkgs\ffmpeg-4.3.1-ha925a31_0\Library\bin\ffmpeg.exe")
audio_controller = AudioController(ffmpeg_path=r"C:\Users\HP\anaconda3\pkgs\ffmpeg-4.3.1-ha925a31_0\Library\bin\ffmpeg.exe")

st.title("Document, Video, and Audio Translator")

# Input options
input_type = st.selectbox("Choose input type", ["Text", "PDF", "Video", "Audio", "Text File"])
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

    if video_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(video_file.read())
            temp_video_path = temp_video.name
        
        try:
            duration = video_controller.get_video_duration(temp_video_path)
            st.write(f"La durée de la vidéo est de {duration} secondes.")
            
            translate_option = st.radio("Choisissez une option de traduction :", 
                                        ("Toute la vidéo", "Une plage de temps spécifique"))
            
            start_second, end_second = None, None
            if translate_option == "Une plage de temps spécifique":
                col1, col2 = st.columns(2)
                with col1:
                    start_second = st.number_input("De la seconde :", 
                                                   min_value=0, max_value=duration-1, value=0)
                with col2:
                    end_second = st.number_input("À la seconde :", 
                                                 min_value=start_second+1, max_value=duration, value=min(start_second+60, duration))

            if st.button("Transcrire et Traduire la Vidéo"):
                with st.spinner("Traitement de la vidéo en cours..."):
                    result = video_controller.transcribe_and_translate_video(temp_video_path, input_lang, output_lang, start_second, end_second)
                    if result["status"] == "success":
                        st.text_area("Transcription", result["transcription"], height=200)
                        st.text_area("Traduction", result["translation"], height=200)
                        
                        # Ajout de l'option de téléchargement des résultats
                        result_text = f"Transcription:\n{result['transcription']}\n\nTraduction:\n{result['translation']}"
                        st.download_button(
                            label="Télécharger les résultats",
                            data=result_text.encode('utf-8'),
                            file_name="video_translation_results.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error(f"Une erreur s'est produite : {result['message']}")
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
elif input_type == "Text File":
    text_file = st.file_uploader("Upload Text file", type=["txt"])

    if text_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="wb") as temp_txt:
            temp_txt.write(text_file.getvalue())
            temp_txt_path = temp_txt.name
        
        try:
            file_content = read_text_file(temp_txt_path)
            total_lines = len(file_content.splitlines())
            st.write(f"Le fichier contient {total_lines} lignes.")
            
            translate_option = st.radio("Choisissez une option de traduction :", 
                                        ("Tout le fichier", "Une plage de lignes spécifique"))
            
            start_line, end_line = None, None
            if translate_option == "Une plage de lignes spécifique":
                col1, col2 = st.columns(2)
                with col1:
                    start_line = st.number_input("De la ligne :", 
                                                 min_value=1, max_value=total_lines, value=1)
                with col2:
                    end_line = st.number_input("À la ligne :", 
                                               min_value=start_line, max_value=total_lines, value=min(start_line+10, total_lines))

            if st.button("Traduire le fichier texte"):
                with st.spinner("Traduction en cours..."):
                    result = text_file_controller.translate_text_file(temp_txt_path, input_lang, output_lang, start_line, end_line)
                    if result["status"] == "success":
                        st.text_area("Texte traduit", result["translated_text"], height=300)
                        
                        # Ajout de l'option de téléchargement du texte traduit
                        translated_file = result["translated_text"].encode('utf-8')
                        st.download_button(
                            label="Télécharger la traduction",
                            data=translated_file,
                            file_name="traduction.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error(f"Une erreur s'est produite : {result['message']}")
        finally:
            os.remove(temp_txt_path)
