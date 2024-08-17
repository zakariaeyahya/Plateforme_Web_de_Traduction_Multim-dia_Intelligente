import torch

def translate_text(text, src_lang, tgt_lang, processor, model, device, language_map, clean_output_func):
    src_lang_code = language_map.get(src_lang.lower().strip(), src_lang)
    tgt_lang_code = language_map.get(tgt_lang.lower().strip(), tgt_lang)
    
    inputs = processor(text=text, src_lang=src_lang_code, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model.generate(**inputs, tgt_lang=tgt_lang_code, generate_speech=False)
    
    token_ids = outputs.sequences[0].cpu().tolist()
    translated_text = clean_output_func(processor.decode(token_ids))
    
    return translated_text