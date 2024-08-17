import os
import subprocess

def compress_video(input_path, output_path, target_size_mb=200, ffmpeg_path=None):
    if not os.path.exists(input_path):
        print(f"Le fichier vidéo n'existe pas : {input_path}")
        return None

    input_size = os.path.getsize(input_path) / (1024 * 1024)  # Taille en MB
    if input_size <= target_size_mb:
        print("La vidéo est déjà plus petite que la taille cible. Pas de compression nécessaire.")
        return input_path

    try:
        duration = float(subprocess.check_output([ffmpeg_path, '-i', input_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0']).decode('utf-8').strip())
        target_bitrate = int((target_size_mb * 8192) / duration)  # en kbps

        output_path = output_path or input_path.rsplit('.', 1)[0] + '_compressed.mp4'
        subprocess.run([
            ffmpeg_path,
            '-i', input_path,
            '-b:v', f'{target_bitrate}k',
            '-maxrate', f'{target_bitrate * 2}k',
            '-bufsize', f'{target_bitrate * 4}k',
            '-c:v', 'libx264',
            '-preset', 'slow',
            '-c:a', 'aac',
            '-b:a', '128k',
            output_path
        ], check=True)

        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la compression de la vidéo : {e}")
        return None