import torch
from transformers import AutoProcessor, SeamlessM4Tv2Model
import logging
import os
import soundfile as sf
from .service_functions.clean_output import clean_output
from .service_functions.translate_text import translate_text
from .service_functions.speech_to_text import speech_to_text
from .service_functions.translate_pdf import translate_pdf
from .service_functions.transcribe_and_translate_video import transcribe_and_translate_video
from .service_functions.process_audio import process_audio
from .service_functions.convert_opus_to_wav import convert_opus_to_wav
from .service_functions.convert_mp3_to_wav import convert_mp3_to_wav
import os
import csv
import librosa
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeamlessTranslator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SeamlessTranslator, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        logger.info("Initialisation de SeamlessTranslator")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Utilisation de l'appareil : {self.device}")
        
        self.processor = None
        self.model = None
        
        self.language_map = {
            "français": "fra",
            "anglais": "eng",
            "arabe": "arb",
            "darija": "ary"
        }
        self._initialized = True
        logger.info("Initialisation terminée")

    def _load_model(self):
        if self.processor is None or self.model is None:
            logger.info("Chargement du modèle et du processeur")
            self.processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
            self.model = SeamlessM4Tv2Model.from_pretrained("facebook/seamless-m4t-v2-large").to(self.device)
            logger.info("Modèle et processeur chargés")

    def translate_text(self, text, src_lang, tgt_lang):
        self._load_model()
        logger.info(f"Traduction de texte : {src_lang} -> {tgt_lang}")
        return translate_text(text, src_lang, tgt_lang, self.processor, self.model, 
                              self.device, self.language_map, clean_output)

    def speech_to_text(self, audio_array, src_lang):
        self._load_model()
        logger.info(f"Transcription audio en {src_lang}")
        return speech_to_text(audio_array, src_lang, self.processor, self.model, 
                              self.device, self.language_map)

    def translate_pdf(self, pdf_path, src_lang, tgt_lang):
        self._load_model()
        logger.info(f"Traduction de PDF : {src_lang} -> {tgt_lang}")
        return translate_pdf(pdf_path, src_lang, tgt_lang, self.translate_text)

    def transcribe_and_translate_video(self, video_path, ffmpeg_path, src_lang, tgt_lang):
        self._load_model()
        logger.info(f"Transcription et traduction de vidéo : {src_lang} -> {tgt_lang}")
        return transcribe_and_translate_video(
            video_path, ffmpeg_path, src_lang, tgt_lang,
            self.speech_to_text, self.translate_text
        )

    def process_audio(self, audio_path, ffmpeg_path, src_lang, tgt_lang, output_csv, audio_type, start_second=None, end_second=None):
        self._load_model()
        logger.info(f"Traitement audio : {src_lang} -> {tgt_lang}")
        
        # Convertir en WAV si nécessaire
        if audio_type == 'wav':
            wav_file_path = audio_path
        else:
            if audio_type == 'mp3':
                wav_file_path = convert_mp3_to_wav(audio_path, ffmpeg_path)
            elif audio_type == 'opus':
                wav_file_path = convert_opus_to_wav(audio_path, ffmpeg_path)
            else:
                return None, None  # Type audio non supporté
        
        if not wav_file_path:
            return None, None
        
        # Charger l'audio
        audio, sr = librosa.load(wav_file_path, sr=None)
        
        # Couper l'audio si nécessaire
        if start_second is not None and end_second is not None:
            start_sample = int(start_second * sr)
            end_sample = int(end_second * sr)
            audio = audio[start_sample:end_sample]
        
        transcription = self.speech_to_text(audio, src_lang)
        translation = self.translate_text(transcription, src_lang, tgt_lang)
        
        # Écrire dans le fichier CSV
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Transcription', 'Translation'])
            writer.writerow([transcription, translation])
        
        return transcription, translation
