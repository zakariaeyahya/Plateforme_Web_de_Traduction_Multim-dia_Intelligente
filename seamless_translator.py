# seamless_translator.py

from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import torch
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeamlessTranslator:
    print("début de la class SeamlessTranslator ")
    def __init__(self):
        print("début de la fonction __ini__")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Utilisation de l'appareil : {self.device}")
        
        self.model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M").to(self.device)
        self.tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
        
        self.language_map = {
            "français": "fr",
            "anglais": "en",
            "arabe": "ar",
            "darija": "ar"  # 'ar' pour darija
        }
        print("fin de la fonctio __ini__")
    
    def translate_text(self, text, src_lang, tgt_lang):
        print("début de la fonction translate_text ")
        src_lang_code = self.language_map.get(src_lang.lower().strip(), src_lang)
        tgt_lang_code = self.language_map.get(tgt_lang.lower().strip(), tgt_lang)
        
        self.tokenizer.src_lang = src_lang_code
        encoded = self.tokenizer(text, return_tensors="pt").to(self.device)
        generated_tokens = self.model.generate(**encoded, forced_bos_token_id=self.tokenizer.get_lang_id(tgt_lang_code))
        result = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        print("fin de la fonction translate_text")
        
        return result
    print("fin de la class SeamlessTranslator")
