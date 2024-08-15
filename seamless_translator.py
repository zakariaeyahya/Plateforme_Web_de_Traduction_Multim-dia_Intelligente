# import torch
import torchaudio
from transformers import AutoProcessor, SeamlessM4Tv2Model
import re
from pydub import AudioSegment
from pathlib import Path
import subprocess
import os
from PyPDF2 import PdfReader
import logging
import torch
import soundfile as sf

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeamlessTranslator:
    def __init__(self):
        print("Début de la fonction __init__...")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Utilisation de l'appareil : {self.device}")
        
        self.processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
        self.model = SeamlessM4Tv2Model.from_pretrained("facebook/seamless-m4t-v2-large").to(self.device)
        
        self.language_map = {
            "français": "fra",
            "anglais": "eng",
            "arabe": "arb",
            "darija": "ary"
        }
        print("Fin de la fonction __init__...")

    def clean_output(self, text):
        print("Début de la fonction clean_output...")
        cleaned_text = text.replace('</s>', '').strip()
        cleaned_text = re.sub(r'__\w+__\s*', '', cleaned_text)
        print("Fin de la fonction clean_output...")
        return cleaned_text

    def translate_text(self, text, src_lang, tgt_lang):
        print("Début de la fonction translate_text...")
        logger.info("Début de la traduction de texte")
        src_lang_code = self.language_map.get(src_lang.lower().strip(), src_lang)
        tgt_lang_code = self.language_map.get(tgt_lang.lower().strip(), tgt_lang)
        
        inputs = self.processor(text=text, src_lang=src_lang_code, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(**inputs, tgt_lang=tgt_lang_code, generate_speech=False)
        
        token_ids = outputs.sequences[0].cpu().tolist()
        translated_text = self.clean_output(self.processor.decode(token_ids))
        logger.info("Fin de la traduction de texte")
        print("Fin de la fonction translate_text...")
        return translated_text

    def speech_to_text(self, audio_array, src_lang):
        print("Début de la fonction speech_to_text...")
        logger.info("Début de la transcription audio")
        src_lang_code = self.language_map.get(src_lang.lower().strip(), src_lang)
        inputs = self.processor(audios=audio_array, return_tensors="pt", sampling_rate=16000).to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(**inputs, tgt_lang=src_lang_code, generate_speech=False)
        token_ids = outputs.sequences[0].cpu().tolist()
        transcription = self.clean_output(self.processor.decode(token_ids))
        logger.info("Fin de la transcription audio")
        print("Fin de la fonction speech_to_text...")
        return transcription

    def extract_text_from_pdf(self, pdf_path):
        print("Début de la fonction extract_text_from_pdf...")
        logger.info(f"Début de l'extraction de texte du PDF: {pdf_path}")
        if not os.path.isfile(pdf_path):
            logger.error(f"Fichier non trouvé: {pdf_path}")
            print("Fin de la fonction extract_text_from_pdf...")
            return ""
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PdfReader(file)
                text = "\n".join(page.extract_text() for page in reader.pages)
                logger.info("Fin de l'extraction de texte du PDF")
                print("Fin de la fonction extract_text_from_pdf...")
                return text
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction du texte du PDF: {e}")
            print("Fin de la fonction extract_text_from_pdf...")
            return ""

    def translate_pdf(self, pdf_path, src_lang, tgt_lang):
        print("Début de la fonction translate_pdf...")
        logger.info(f"Début de la traduction du PDF: {pdf_path}")
        text = self.extract_text_from_pdf(pdf_path)
        if text:
            translated_text = self.translate_text(text, src_lang, tgt_lang)
            logger.info("Fin de la traduction du PDF")
            print("Fin de la fonction translate_pdf...")
            return translated_text
        else:
            logger.error("Pas de texte à traduire dans le PDF.")
            print("Fin de la fonction translate_pdf...")
            return ""

    def convert_mp4_to_wav(self, mp4_file_path, ffmpeg_path):
        print("Début de la fonction convert_mp4_to_wav...")
        logger.info(f"Début de la conversion MP4 vers WAV: {mp4_file_path}")
        wav_file_path = os.path.splitext(mp4_file_path)[0] + '.wav'
        try:
            subprocess.run([ffmpeg_path, '-i', mp4_file_path, '-acodec', 'pcm_s16le', '-ar', '16000', wav_file_path], check=True)
            logger.info(f"Conversion réussie de {mp4_file_path} vers {wav_file_path}")
            print("Fin de la fonction convert_mp4_to_wav...")
            return wav_file_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Échec de la conversion de {mp4_file_path} vers WAV: {e}")
            print("Fin de la fonction convert_mp4_to_wav...")
            return None

    def transcribe_and_translate_video(self, video_path, ffmpeg_path, src_lang, tgt_lang):
        logger.info(f"Début de la transcription et traduction de la vidéo: {video_path}")
        wav_file_path = self.convert_mp4_to_wav(video_path, ffmpeg_path)
        if not wav_file_path:
            logger.error("La conversion de la vidéo a échoué.")
            return None, None

        try:
            # Utiliser soundfile pour lire le fichier WAV
            audio_array, sample_rate = sf.read(wav_file_path)
            
            # Assurez-vous que l'audio est mono
            if len(audio_array.shape) > 1:
                audio_array = audio_array.mean(axis=1)
            
            transcription = self.speech_to_text(audio_array, src_lang)
            translation = self.translate_text(transcription, src_lang, tgt_lang)
            logger.info("Fin de la transcription et traduction de la vidéo")
            return transcription, translation
        except Exception as e:
            logger.error(f"Une erreur s'est produite lors de la transcription ou de la traduction: {e}")
            return None, None
        finally:
            if os.path.exists(wav_file_path):
                os.remove(wav_file_path)
                logger.info(f"Fichier WAV temporaire supprimé: {wav_file_path}")

# import torch
