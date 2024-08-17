import os
from .convert_mp4_to_wav import convert_mp4_to_wav
from .compress_video import compress_video
from .process_wav import process_wav

def transcribe_and_translate_video(video_path, ffmpeg_path, src_lang, tgt_lang, speech_to_text_func, translate_text_func):
    video_size_mb = os.path.getsize(video_path) / (1024 * 1024)
    if video_size_mb > 200:
        print(f"La vidéo dépasse 200 MB. Compression en cours...")
        compressed_video_path = compress_video(video_path, None, 200, ffmpeg_path)
        if compressed_video_path:
            video_path = compressed_video_path
        else:
            print("La compression de la vidéo a échoué. Utilisation de la vidéo originale.")

    wav_file_path = convert_mp4_to_wav(video_path, ffmpeg_path)
    if not wav_file_path:
        print("La conversion de la vidéo a échoué.")
        return None, None

    try:
        return process_wav(speech_to_text_func, translate_text_func, wav_file_path, src_lang, tgt_lang)
    finally:
        if os.path.exists(wav_file_path):
            os.remove(wav_file_path)
        if video_path != video_path and os.path.exists(video_path):
            os.remove(video_path)