# interface.py

import streamlit as st
from seamless_translator import SeamlessTranslator

# Initialisation du traducteur
translator = SeamlessTranslator()

# Interface Streamlit
st.title("Traducteur Multilingue avec Seamless Translator")

# Entrée de texte
input_text = st.text_area("Entrez le texte à traduire", value="Bonjour, comment ça va ?")

# Sélection des langues
input_lang = st.selectbox("Langue source", ["français", "anglais", "arabe", "darija"])
output_lang = st.selectbox("Langue cible", ["français", "anglais", "arabe", "darija"])

# Bouton pour effectuer la traduction
if st.button("Traduire"):
    translated_text = translator.translate_text(input_text, input_lang, output_lang)
    
    # Affichage du résultat
    st.subheader(f"Texte original ({input_lang}) :")
    st.write(input_text)
    
    st.subheader(f"Traduction ({output_lang}) :")
    st.write(translated_text)
