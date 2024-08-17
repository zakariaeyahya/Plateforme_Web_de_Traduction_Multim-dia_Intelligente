import torch

def speech_to_text(audio_array, src_lang, processor, model, device, language_map):
    src_lang_code = language_map.get(src_lang.lower().strip(), src_lang)
    inputs = processor(audios=audio_array, return_tensors="pt", sampling_rate=16000).to(device)
    with torch.no_grad():
        outputs = model.generate(**inputs, tgt_lang=src_lang_code, generate_speech=False)
    token_ids = outputs.sequences[0].cpu().tolist()
    transcription = processor.decode(token_ids)
    return transcription