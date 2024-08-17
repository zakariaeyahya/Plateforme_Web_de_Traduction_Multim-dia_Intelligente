import subprocess
import os
import tempfile

def convert_mp3_to_wav(mp3_file_path, ffmpeg_path):
        # Créer un nouveau fichier temporaire pour la sortie WAV
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
        wav_file_path = temp_wav.name
    try:
        subprocess.run([
            ffmpeg_path,
            '-y',  # Force overwrite without asking
            '-i', mp3_file_path,
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-ac', '1',
            wav_file_path
        ], check=True, stderr=subprocess.PIPE)
        return wav_file_path
    except subprocess.CalledProcessError as e:
        print(f"Échec de la conversion de {mp3_file_path} vers WAV: {e}")
        print(f"Stderr: {e.stderr.decode()}")
        return None