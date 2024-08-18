import os
import librosa
from services.service_seamless import SeamlessTranslator
from services.service_functions.clean_output import clean_output

class AudioController:
    def __init__(self, ffmpeg_path):
        self.translator = SeamlessTranslator()
        self.ffmpeg_path = ffmpeg_path

    def get_audio_duration(self, audio_path):
        duration = librosa.get_duration(filename=audio_path)
        return int(duration)

    def process_audio(self, audio_path, src_lang, tgt_lang, output_csv, audio_type, start_second=None, end_second=None):
        try:
            if not os.path.exists(audio_path):
                return {"status": "error", "message": "Audio file not found"}
            
            duration = self.get_audio_duration(audio_path)
            
            if start_second is not None and end_second is not None:
                if start_second < 0 or end_second > duration or start_second >= end_second:
                    return {"status": "error", "message": f"Invalid time range. The audio duration is {duration} seconds."}
            
            transcription, translation = self.translator.process_audio(
                audio_path, self.ffmpeg_path, src_lang, tgt_lang, output_csv, audio_type, start_second, end_second
            )
            
            if transcription is None or translation is None:
                return {"status": "error", "message": "Audio processing failed"}
            
            transcription = clean_output(transcription)
            translation = clean_output(translation)
            
            return {
                "status": "success",
                "transcription": transcription,
                "translation": translation,
                "csv_path": output_csv,
                "duration": duration
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
