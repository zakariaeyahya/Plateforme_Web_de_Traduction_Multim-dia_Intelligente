import re

def clean_output(text):
    cleaned_text = text.replace("<unk>", "").replace("</s>", "").strip()
    cleaned_text = re.sub(r'__\w+__\s*', '', cleaned_text)
    return cleaned_text
