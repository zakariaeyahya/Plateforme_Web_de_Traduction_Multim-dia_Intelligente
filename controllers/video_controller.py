import os
from services.service_seamless import SeamlessTranslator

class VideoController:
    def __init__(self, ffmpeg_path):
        self.translator = SeamlessTranslator()
        self.ffmpeg_path = ffmpeg_path

    def transcribe_and_translate_video(self, video_path, src_lang, tgt_lang):
        try:
            if not os.path.exists(video_path):
                return {"status": "error", "message": "Video file not found"}
            
            transcription, translation = self.translator.transcribe_and_translate_video(
                video_path, self.ffmpeg_path, src_lang, tgt_lang
            )
            transcription = clean_output(transcription)
            translation = clean_output(translation)
            return {
                "status": "success",
                "transcription": transcription,
                "translation": translation
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
