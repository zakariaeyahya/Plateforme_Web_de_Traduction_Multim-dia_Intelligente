import os
from services.service_seamless import SeamlessTranslator
from services.service_functions.clean_output import clean_output

class AudioController:
    def __init__(self, ffmpeg_path):
        self.translator = SeamlessTranslator()
        self.ffmpeg_path = ffmpeg_path

    def process_audio(self, audio_path, src_lang, tgt_lang, output_csv, audio_type):
        try:
            if not os.path.exists(audio_path):
                return {"status": "error", "message": "Audio file not found"}
            
            transcription, translation = self.translator.process_audio(
                audio_path, self.ffmpeg_path, src_lang, tgt_lang, output_csv, audio_type
            )
            
            if transcription is None or translation is None:
                return {"status": "error", "message": "Audio processing failed"}
            
            # Clean the output after processing
            transcription = clean_output(transcription)
            translation = clean_output(translation)
            
            return {
                "status": "success",
                "transcription": transcription,
                "translation": translation,
                "csv_path": output_csv
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}