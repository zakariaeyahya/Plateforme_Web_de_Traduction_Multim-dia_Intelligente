import os
import datetime
import csv
from .convert_mp3_to_wav import convert_mp3_to_wav
from .process_wav import process_wav

def process_audio(audio_path, ffmpeg_path, src_lang, tgt_lang, output_csv, speech_to_text_func, translate_text_func):
    wav_file_path = convert_mp3_to_wav(audio_path, ffmpeg_path)
    if not wav_file_path:
        print("La conversion de l'audio a échoué.")
        return None, None

    try:
        transcription, translation = process_wav(speech_to_text_func, translate_text_func, wav_file_path, src_lang, tgt_lang)
        
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Filename', 'Transcription', 'Translation', 'Timestamp'])
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            csvwriter.writerow([os.path.basename(audio_path), transcription, translation, timestamp])
        
        return transcription, translation
    except Exception as e:
        print(f"Une erreur s'est produite lors du traitement audio: {e}")
        return None, None
    finally:
        if os.path.exists(wav_file_path):
            os.remove(wav_file_path)