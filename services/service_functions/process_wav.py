import soundfile as sf

def process_wav(speech_to_text_func, translate_text_func, wav_file_path, src_lang, tgt_lang):
    audio_array, sample_rate = sf.read(wav_file_path)
    
    if len(audio_array.shape) > 1:
        audio_array = audio_array.mean(axis=1)
    
    segment_length = 10 * sample_rate
    segments = [audio_array[i:i+segment_length] for i in range(0, len(audio_array), segment_length)]
    
    transcriptions = []
    translations = []
    
    for i, segment in enumerate(segments):
        segment_transcription = speech_to_text_func(segment, src_lang)
        transcriptions.append(segment_transcription)
        
        segment_translation = translate_text_func(segment_transcription, src_lang, tgt_lang)
        translations.append(segment_translation)
    
    full_transcription = " ".join(transcriptions)
    full_translation = " ".join(translations)
    
    return full_transcription, full_translation