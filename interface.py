import streamlit as st
import tempfile
import os

from controllers.text_controller import TextController
from controllers.pdf_controller import PDFController
from controllers.video_controller import VideoController
from controllers.audio_controller import AudioController
from controllers.text_file_controller import TextFileController
from services.service_functions import clean_output
from services.service_functions.text_file_functions import read_text_file

# Initialize controllers with necessary configurations
FFMPEG_PATH = r"C:\Users\HP\anaconda3\pkgs\ffmpeg-4.3.1-ha925a31_0\Library\bin\ffmpeg.exe"
text_controller = TextController()
pdf_controller = PDFController()
text_file_controller = TextFileController()
video_controller = VideoController(ffmpeg_path=FFMPEG_PATH)
audio_controller = AudioController(ffmpeg_path=FFMPEG_PATH)

# Streamlit page configuration
st.set_page_config(page_title="Traducteur Multimédia", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .main-title {
        font-size: 3em;
        color: #1E90FF;
        text-align: center;
        margin-bottom: 30px;
    }
    .sub-title {
        font-size: 1.5em;
        color: #4682B4;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        font-size: 16px;
        border: none;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        background-color: #F0F8FF;
    }
    .output-area {
        background-color: #F0F8FF;
        padding: 10px;
        border-radius: 5px;
        margin-top: 20px;
    }
    .content {
        font-size: 1.1em;
        line-height: 1.6;
    }
    .sidebar-nav {
        padding: 10px;
        border-radius: 10px;
        background-color: #f0f2f6;
    }
    .sidebar-nav h1 {
        color: #1E90FF;
        font-size: 24px;
        margin-bottom: 20px;
        text-align: center;
    }
    .nav-item {
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .nav-item:hover {
        background-color: #e0e2e6;
    }
    .nav-item.active {
        background-color: #1E90FF;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation setup
st.sidebar.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
st.sidebar.markdown('<h1>Navigation</h1>', unsafe_allow_html=True)

# Define the available pages
pages = {
    "Accueil": "Accueil",
    "Traduction": "Traduction",
    "À Propos": "À Propos"
}

# Initialize session state if it doesn't exist
if "page" not in st.session_state:
    st.session_state.page = "Accueil"

# Use a radio button for navigation
page = st.sidebar.radio(
    "",
    options=list(pages.keys()),
    key="page",
    label_visibility="collapsed"
)

# No need to set st.session_state.page here; it's already managed by the radio button

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Page-specific content rendering
if page == "Accueil":
    st.markdown("<h1 class='main-title'>Traducteur Multimédia Spécialisé en Darija 🇲🇦</h1>", unsafe_allow_html=True)
    st.markdown("*\"Connecter le Maroc au monde, un mot à la fois.\"*")

    st.header("🌟 Notre Mission")
    st.write("""
    Bienvenue dans notre projet innovant de Traducteur Multimédia, spécialement conçu pour briser les barrières linguistiques 
    entre le darija marocain et les langues du monde entier. Notre mission est de faciliter la communication, la compréhension 
    et l'échange culturel en rendant le darija accessible à tous, et en ouvrant le Maroc aux langues internationales.
    """)

    st.header("🚀 Pourquoi le Darija ?")
    st.write("""
    Le darija, dialecte  marocain, est au cœur de la culture et de la communication quotidienne au Maroc. Cependant, 
    sa richesse et sa complexité peuvent être un défi pour les non-locuteurs. Notre traducteur est conçu pour :
    
    - Faciliter la compréhension du darija pour les visiteurs et les entreprises internationales
    - Aider les Marocains à communiquer plus efficacement à l'échelle mondiale
    - Préserver et promouvoir la richesse linguistique du Maroc
    """)

    st.header("🛠 Nos Fonctionnalités Uniques")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📝 Texte Darija Intelligent")
        st.write("Notre IA comprend les nuances et les expressions idiomatiques du darija, assurant des traductions précises et naturelles.")
        
        st.subheader("🎥 Vidéos en Darija Décodées")
        st.write("Transformez vos vidéos en darija avec des sous-titres et des traductions dans de nombreuses langues.")
    with col2:
        st.subheader("🔊 Audio Darija Amplifié")
        st.write("Transcrivez et traduisez des conversations en darija, rendant les podcasts et les enregistrements accessibles à tous.")
        
        st.subheader("📚 Documents Multilingues")
        st.write("Traduisez des documents officiels, des articles et des livres du darija vers d'autres langues et vice versa.")

    st.header("🌍 Impact sur la Communication Interculturelle")
    st.write("""
    Notre projet vise à :
    1. Renforcer les liens économiques en facilitant la communication d'affaires
    2. Promouvoir le tourisme en rendant le Maroc plus accessible linguistiquement
    3. Faciliter les échanges éducatifs et culturels internationaux
    4. Préserver et partager la richesse du patrimoine linguistique marocain
    """)

    st.header("🚀 Comment Utiliser Notre Traducteur")
    st.markdown("""
    1. 🧭 Naviguez vers l'onglet "Traduction" dans le menu latéral.
    2. 📊 Sélectionnez votre type de média (texte, audio, vidéo, document).
    3. 🌐 Choisissez le darija comme langue source ou cible.
    4. 📤 Téléchargez votre fichier ou entrez votre texte en darija.
    5. ✨ Laissez notre IA travailler sa magie et découvrez votre traduction !
    """)

    st.header("🔮 L'Avenir de la Traduction Darija")
    st.write("""
    Nous travaillons continuellement à l'amélioration de notre technologie pour:
    - Intégrer plus de variations régionales du darija
    - Développer des modèles de traduction spécifiques à différents domaines (médical, juridique, technique)
    - Créer des outils d'apprentissage du darija basés sur l'IA
    
    Rejoignez-nous dans cette aventure linguistique passionnante et contribuez à rapprocher les cultures grâce à la puissance de la traduction !
    """)

    st.markdown("---")
    st.markdown("<p style='text-align: center;'>Développé avec passion par  YAHYA ZAKARIAE </p>", unsafe_allow_html=True)
elif page == "Traduction":
    st.markdown("<h1 class='main-title'>Traducteur Multimédia</h1>", unsafe_allow_html=True)

    # Input type selection
    input_type = st.selectbox("Choisissez le type d'entrée", ["Texte", "Fichier PDF", "Vidéo", "Audio", "Fichier Texte"])

    # Language selection
    col1, col2 = st.columns(2)
    with col1:
        input_lang = st.selectbox("Langue source", ["français", "anglais", "arabe", "darija"])
    with col2:
        output_lang = st.selectbox("Langue cible", ["français", "anglais", "arabe", "darija"])

    # Processing based on input type
    if input_type == "Texte":
        st.markdown("<h2 class='sub-title'>Traduction de Texte</h2>", unsafe_allow_html=True)
        input_text = st.text_area("Entrez le texte à traduire")

        if st.button("Traduire le Texte"):
            with st.spinner("Traduction en cours..."):
                result = text_controller.translate_text(input_text, input_lang, output_lang)
                if result["status"] == "success":
                    st.markdown("<div class='output-area'>", unsafe_allow_html=True)
                    st.text_area("Texte traduit", result["translated_text"], height=200)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error(f"Une erreur s'est produite : {result['message']}")

    elif input_type == "Fichier PDF":
        st.markdown("<h2 class='sub-title'>Traduction de PDF</h2>", unsafe_allow_html=True)
        pdf_file = st.file_uploader("Téléchargez le fichier PDF", type=["pdf"])

        if pdf_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(pdf_file.read())
                temp_pdf_path = temp_pdf.name
            
            try:
                paragraph_count, _ = pdf_controller.count_paragraphs_in_pdf(temp_pdf_path)
                st.write(f"Le PDF contient {paragraph_count} paragraphes.")
                
                translate_option = st.radio("Choisissez une option de traduction :", 
                                            ("Tout le PDF", "Une plage de paragraphes"))
                
                start_paragraph, end_paragraph = None, None
                if translate_option == "Une plage de paragraphes":
                    col1, col2 = st.columns(2)
                    with col1:
                        start_paragraph = st.number_input("Du paragraphe :", 
                                                          min_value=1, max_value=paragraph_count, value=1)
                    with col2:
                        end_paragraph = st.number_input("Au paragraphe :", 
                                                        min_value=start_paragraph, max_value=paragraph_count, value=min(start_paragraph+2, paragraph_count))

                if st.button("Traduire le PDF"):
                    with st.spinner("Traduction en cours..."):
                        result = pdf_controller.translate_pdf(temp_pdf_path, input_lang, output_lang, start_paragraph, end_paragraph)
                        if result["status"] == "success":
                            st.markdown("<div class='output-area'>", unsafe_allow_html=True)
                            st.text_area("Texte traduit", result["translated_text"], height=300)
                            st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            st.error(f"Une erreur s'est produite : {result['message']}")
            finally:
                os.remove(temp_pdf_path)

    elif input_type == "Vidéo":
        st.markdown("<h2 class='sub-title'>Traduction de Vidéo</h2>", unsafe_allow_html=True)
        video_file = st.file_uploader("Téléchargez le fichier vidéo", type=["mp4"])

        if video_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
                temp_video.write(video_file.read())
                temp_video_path = temp_video.name
            
            try:
                duration = video_controller.get_video_duration(temp_video_path)
                st.write(f"La durée de la vidéo est de {duration} secondes.")
                
                translate_option = st.radio("Choisissez une option de traduction :", 
                                            ("Toute la vidéo", "Une plage de temps spécifique"))
                
                start_second, end_second = None, None
                if translate_option == "Une plage de temps spécifique":
                    col1, col2 = st.columns(2)
                    with col1:
                        start_second = st.number_input("De la seconde :", 
                                                       min_value=0, max_value=duration-1, value=0)
                    with col2:
                        end_second = st.number_input("À la seconde :", 
                                                     min_value=start_second+1, max_value=duration, value=min(start_second+60, duration))

                if st.button("Transcrire et Traduire la Vidéo"):
                    with st.spinner("Traitement de la vidéo en cours..."):
                        result = video_controller.transcribe_and_translate_video(temp_video_path, input_lang, output_lang, start_second, end_second)
                        if result["status"] == "success":
                            st.markdown("<div class='output-area'>", unsafe_allow_html=True)
                            st.text_area("Transcription", result["transcription"], height=200)
                            st.text_area("Traduction", result["translation"], height=200)
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            # Add download option for results
                            result_text = f"Transcription:\n{result['transcription']}\n\nTraduction:\n{result['translation']}"
                            st.download_button(
                                label="Télécharger les résultats",
                                data=result_text.encode('utf-8'),
                                file_name="video_translation_results.txt",
                                mime="text/plain"
                            )
                        else:
                            st.error(f"Une erreur s'est produite : {result['message']}")
            finally:
                os.remove(temp_video_path)

    elif input_type == "Audio":
        st.markdown("<h2 class='sub-title'>Traitement Audio</h2>", unsafe_allow_html=True)
        audio_file = st.file_uploader("Téléchargez le fichier audio", type=["mp3", "opus", "wav"])
        audio_type = st.selectbox("Sélectionnez le type audio", ["mp3", "opus", "wav"])

        if audio_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.' + audio_type) as temp_audio:
                temp_audio.write(audio_file.read())
                temp_audio_path = temp_audio.name
            
            try:
                duration = audio_controller.get_audio_duration(temp_audio_path)
                st.write(f"La durée de l'audio est de {duration} secondes.")
                
                translate_option = st.radio("Choisissez une option de traduction :", 
                                            ("Tout l'audio", "Une plage de temps spécifique"))
                
                start_second, end_second = None, None
                if translate_option == "Une plage de temps spécifique":
                    col1, col2 = st.columns(2)
                    with col1:
                        start_second = st.number_input("De la seconde :", 
                                                       min_value=0, max_value=duration-1, value=0)
                    with col2:
                        end_second = st.number_input("À la seconde :", 
                                                     min_value=start_second+1, max_value=duration, value=min(start_second+10, duration))

                if st.button("Transcrire et Traduire l'Audio"):
                    with st.spinner("Traitement audio en cours..."):
                        output_csv = tempfile.NamedTemporaryFile(delete=False, suffix=".csv").name
                        result = audio_controller.process_audio(temp_audio_path, input_lang, output_lang, output_csv, audio_type, start_second, end_second)
                        if result["status"] == "success":
                            st.markdown("<div class='output-area'>", unsafe_allow_html=True)
                            st.text_area("Transcription", result["transcription"], height=200)
                            st.text_area("Traduction", result["translation"], height=200)
                            st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            st.error(f"Une erreur s'est produite : {result['message']}")
            finally:
                os.remove(temp_audio_path)
                if 'output_csv' in locals() and os.path.exists(output_csv):
                    os.remove(output_csv)

    elif input_type == "Fichier Texte":
        st.markdown("<h2 class='sub-title'>Traduction de Fichier Texte</h2>", unsafe_allow_html=True)
        text_file = st.file_uploader("Téléchargez le fichier texte", type=["txt"])

        if text_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_txt:
                temp_txt.write(text_file.read())
                temp_txt_path = temp_txt.name
            
            try:
                file_content = read_text_file(temp_txt_path)
                total_lines = len(file_content.splitlines())
                st.write(f"Le fichier contient {total_lines} lignes.")
                
                translate_option = st.radio("Choisissez une option de traduction :", 
                                            ("Tout le fichier", "Une plage de lignes spécifique"))
                
                start_line, end_line = None, None
                if translate_option == "Une plage de lignes spécifique":
                    col1, col2 = st.columns(2)
                    with col1:
                        start_line = st.number_input("De la ligne :", 
                                                     min_value=1, max_value=total_lines, value=1)
                    with col2:
                        end_line = st.number_input("À la ligne :", 
                                                   min_value=start_line, max_value=total_lines, value=min(start_line+10, total_lines))

                if st.button("Traduire le fichier texte"):
                    with st.spinner("Traduction en cours..."):
                        result = text_file_controller.translate_text_file(temp_txt_path, input_lang, output_lang, start_line, end_line)
                        if result["status"] == "success":
                            st.markdown("<div class='output-area'>", unsafe_allow_html=True)
                            st.text_area("Texte traduit", result["translated_text"], height=300)
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            # Add download option for translated text
                            translated_file = result["translated_text"].encode('utf-8')
                            st.download_button(
                                label="Télécharger la traduction",
                                data=translated_file,
                                file_name="traduction.txt",
                                mime="text/plain"
                            )
                        else:
                            st.error(f"Une erreur s'est produite : {result['message']}")
            finally:
                os.remove(temp_txt_path)

elif page == "À Propos":
    st.markdown("<h1 class='main-title'>À Propos du Projet 🌟</h1>", unsafe_allow_html=True)

    st.markdown("## 📚 Résumé du Projet")

    st.markdown("🚀 Le Traducteur Multimédia est une initiative novatrice visant à transformer radicalement l'approche de la traduction dans notre ère numérique globalisée. En exploitant les dernières avancées en matière de traitement du langage naturel et d'intelligence artificielle, notre plateforme propose une solution intégrée et polyvalente pour transcender les barrières linguistiques à travers une multitude de formats médias.")

    st.markdown("🌍 Notre ambition est de façonner un monde où la diversité linguistique enrichit la communication plutôt que de l'entraver. Que ce soit dans un cadre professionnel, éducatif ou personnel, notre outil est conçu pour démocratiser l'accès à une traduction rapide, précise et contextuelle, favorisant ainsi une compréhension mutuelle sans précédent.")

    st.markdown("💡 L'unicité de notre projet réside dans sa capacité à traiter un large éventail de supports : du texte brut aux documents PDF, en passant par les contenus vidéo et audio. Cette approche holistique offre aux utilisateurs la flexibilité de traduire des contenus variés, catalysant ainsi les échanges d'informations et la collaboration à l'échelle internationale. En repoussant les frontières de la traduction conventionnelle, nous ouvrons la voie à une nouvelle ère de communication interculturelle fluide et enrichissante.")

    st.markdown("<h2 class='sub-title'>🛠️ Fonctionnalités Clés</h2>", unsafe_allow_html=True)


    st.markdown("""
    <div class='content'>
        <ul>
            <li>📝 Traduction de texte avec prise en charge de multiples langues</li>
            <li>📄 Traduction de fichiers PDF avec option de sélection de plages de paragraphes</li>
            <li>🎥 Transcription et traduction de fichiers vidéo</li>
            <li>🎵 Traitement et traduction de fichiers audio</li>
            <li>📁 Traduction de fichiers texte avec option de sélection de plages de lignes</li>
            <li>🔄 Interface utilisateur intuitive et conviviale</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 class='sub-title'>🔮 Travaux Futurs</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class='content'>
        <p>🌱 Notre projet est en constante évolution, et nous avons de nombreuses idées passionnantes pour l'avenir :</p>
        <ul>
            <li>🌐 Intégration de plus de langues et de dialectes, avec un focus particulier sur les langues moins représentées</li>
            <li>🧠 Amélioration de la précision de la traduction grâce à des modèles de langage plus avancés et à l'apprentissage continu</li>
            <li>⚡ Ajout de fonctionnalités de traduction en temps réel pour les flux audio et vidéo, idéal pour les conférences et les webinaires</li>
            <li>🔗 Développement d'une API robuste pour permettre l'intégration transparente avec d'autres applications et services</li>
            <li>🎨 Refonte de l'interface utilisateur pour une expérience encore plus intuitive et personnalisable</li>
            <li>📊 Intégration d'outils d'analyse avancés pour fournir des insights sur les traductions et l'utilisation</li>
            <li>📱 Développement d'applications mobiles pour iOS et Android pour une accessibilité accrue</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 class='sub-title'>🤝 Contribuer au Projet</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class='content'>
        <p>🌟 Nous croyons en la puissance de la collaboration et de l'open source. Si vous êtes passionné par les langues, 
        la technologie ou simplement intéressé par notre projet, il existe plusieurs façons de contribuer :</p>
        <ul>
            <li>💻 Contribuer au code source sur notre dépôt GitHub</li>
            <li>🔍 Tester l'application et signaler des bugs ou suggérer des améliorations</li>
            <li>📖 Aider à améliorer la documentation et les guides d'utilisation</li>
            <li>🌍 Participer à la traduction de l'interface utilisateur dans différentes langues</li>
            <li>💡 Proposer de nouvelles idées de fonctionnalités ou d'améliorations</li>
        </ul>
        <p>Chaque contribution, quelle que soit sa taille, est précieuse et appréciée !</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 class='sub-title'>📬 Contact</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class='content'>
        <p>🧑‍💻 Ce projet a été développé avec passion par Yahya Zakariae. Pour toute question, suggestion ou opportunité de collaboration, n'hésitez pas à me contacter :</p>
        <ul>
            <li>📧 Email : zakariae.yh@gmail.com </li>
            <li>🔗 LinkedIn : <a href="https://www.linkedin.com/in/zakariae-yahya/">linkedin.com/in/yahyazakariae</a></li>
            <li>🐱 GitHub : <a href="https://github.com/zakariaeyahya">github.com/yahyazakariae</a></li>
        </ul>
        <p>💬 Je suis toujours ouvert aux retours, aux idées et aux discussions sur la façon d'améliorer cette application et 
        de la rendre encore plus utile pour notre communauté mondiale. N'hésitez pas à partager vos pensées et vos expériences !</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 class='sub-title'>🙏 Remerciements</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class='content'>
        <p>Un grand merci à tous ceux qui ont contribué à ce projet, que ce soit par leur code, leurs idées ou leur soutien. 
        Ce projet n'aurait pas été possible sans la riche communauté open-source et les nombreuses bibliothèques et 
        frameworks sur lesquels il s'appuie.</p>
        <p>Ensemble, continuons à construire des ponts entre les langues et les cultures ! 🌉🌍</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center;'>Développé avec ❤️ par Yahya Zakariae</p>", unsafe_allow_html=True)
