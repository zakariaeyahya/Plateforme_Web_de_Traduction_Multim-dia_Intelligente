import os
import librosa
from services.service_seamless import SeamlessTranslator
from services.service_functions.clean_output import clean_output

class VideoController:
    def __init__(self, ffmpeg_path):
        self.translator = SeamlessTranslator()
        self.ffmpeg_path = ffmpeg_path

    def get_video_duration(self, video_path):
        audio, sr = librosa.load(video_path, sr=None)
        duration = librosa.get_duration(y=audio, sr=sr)
        return int(duration)

    def transcribe_and_translate_video(self, video_path, src_lang, tgt_lang, start_second=None, end_second=None):
        try:
            if not os.path.exists(video_path):
                return {"status": "error", "message": "Video file not found"}
            
            wav_file_path = self.translator.convert_mp4_to_wav(video_path, self.ffmpeg_path)
            if not wav_file_path:
                return {"status": "error", "message": "Failed to convert video to audio"}

            duration = self.get_video_duration(wav_file_path)
            
            if start_second is not None and end_second is not None:
                if start_second < 0 or end_second > duration or start_second >= end_second:
                    return {"status": "error", "message": f"Invalid time range. The video duration is {duration} seconds."}
            
            transcription, translation = self.translator.transcribe_and_translate_video(
                wav_file_path, self.ffmpeg_path, src_lang, tgt_lang, start_second, end_second
            )
            transcription = clean_output(transcription)
            translation = clean_output(translation)
            os.remove(wav_file_path)  # Clean up the temporary WAV file
            
            if transcription is None or translation is None:
                return {"status": "error", "message": "Video processing failed"}
            
            return {
                "status": "success",
                "transcription": transcription,
                "translation": translation,
                "duration": duration
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
