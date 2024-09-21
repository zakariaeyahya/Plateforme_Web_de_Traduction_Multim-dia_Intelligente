# 🌍 Traducteur Multimédia Spécialisé en Darija 🇲🇦
![aWISQ6jhonuvK8tlA-dHq_6d3beed313d74288a8d27334dfc8f6fc](https://github.com/user-attachments/assets/904c0bb5-3c12-466e-b05d-2396250aa750)

## 🌟 À propos du projet

Le Traducteur Multimédia est une application révolutionnaire conçue pour transcender les barrières linguistiques entre le darija marocain et les langues du monde. Notre mission est de catalyser la communication interculturelle, favoriser la compréhension mutuelle et enrichir les échanges en rendant le darija accessible globalement tout en ouvrant le Maroc à la diversité linguistique internationale.

### 🎯 Objectifs clés

- Faciliter l'intégration et la communication des Marocains à l'échelle mondiale
- Promouvoir la richesse culturelle et linguistique du Maroc
- Soutenir le tourisme et les échanges économiques en réduisant les obstacles linguistiques
- Encourager l'apprentissage et l'échange culturel international

## 🚀 Fonctionnalités principales

- 📝 Traduction de texte multilingue avec support avancé du darija
- 📄 Traduction intelligente de fichiers PDF avec sélection de plages de paragraphes
- 🎥 Transcription et traduction de contenu vidéo
- 🎵 Traitement et traduction de fichiers audio
- 📁 Traduction de fichiers texte avec option de sélection de plages spécifiques
- 🔄 Interface utilisateur intuitive et conviviale

## 💡 Avantages uniques

- 🌐 Spécialisation en darija marocain, comblant une lacune importante dans les services de traduction existants
- 🧠 Utilisation d'algorithmes d'IA avancés pour une compréhension contextuelle et culturelle approfondie
- 🔍 Haute précision dans la traduction des expressions idiomatiques et des nuances linguistiques
- 📊 Support multimédia complet, offrant une solution tout-en-un pour divers besoins de traduction

## 🛠️ Technologies de pointe

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFB02E?style=for-the-badge&logo=huggingface&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-%23007ACC.svg?style=for-the-badge&logo=ffmpeg&logoColor=white)
## 🏗️ Architecture des fonctionnalités
Notre traducteur multimédia utilise des processus spécialisés pour chaque type de contenu, assurant une traduction précise et contextuelle. Voici un aperçu de l'architecture de chaque fonctionnalité principale :
### 1. Traduction de texte
Le processus de traduction de texte implique plusieurs étapes de prétraitement avant la traduction proprement dite, garantissant une haute qualité de traduction, en particulier pour le darija.
![1](https://github.com/user-attachments/assets/1e3ad770-7b93-40d8-b234-90c5d1d77081)
1. Le texte brut est d'abord analysé pour la détection de langue.
2. Le prétraitement inclut la suppression des caractères spéciaux, la correction orthographique, la tokenisation et la lemmatisation.
3. Le texte prétraité est ensuite traduit.
4.  Un post-traitement peut être appliqué avant de produire le texte final traduit.

### 2. Traduction de PDF
La traduction de documents PDF nécessite des étapes supplémentaires pour gérer la structure et la mise en page du document.
![2](https://github.com/user-attachments/assets/27391e39-ef4c-4dd7-b1bd-fa04d865182c)
1. Le texte est extrait du fichier PDF.
2. La langue du document est détectée.
3. Le texte subit un prétraitement, incluant la segmentation en paragraphes et la normalisation.
4. Le texte prétraité est traduit.
5. Le PDF est reconstitué avec le texte traduit, préservant la mise en page originale.

### 3. Traduction de vidéo
Le processus de traduction vidéo combine traitement audio et visuel pour une expérience de traduction complète.
![3](https://github.com/user-attachments/assets/d3de8040-610f-4d64-83f6-0040df795b57)

1. L'audio est extrait de la vidéo et transcrit.
2. La langue est détectée à partir de la transcription.
3. Le texte transcrit est prétraité et normalisé.
4. La traduction est effectuée sur le texte préparé.
5. Les sous-titres traduits sont synchronisés avec la vidéo originale.

### Traduction audio
La traduction audio implique la conversion de la parole en texte, suivie d'une traduction et potentiellement d'une reconversion en audio.
![4](https://github.com/user-attachments/assets/a744b5a7-30c6-4a58-b345-41f520689ab1)
1. Le fichier audio est transcrit en texte.
2. La langue source est détectée.
3. Le texte transcrit est prétraité, incluant la segmentation en phrases et la normalisation.
4. La traduction est effectuée sur le texte préparé.
5.  Le texte traduit peut être converti en audio via la synthèse vocale (optionnel).

### Traduction de fichiers texte
La traduction de fichiers texte prend en compte la structure du document pour préserver la mise en forme.
![5](https://github.com/user-attachments/assets/b877b122-db66-467f-b94c-03ae0ca22fdc)
1. Le contenu du fichier texte est extrait.
2. La langue du document est détectée.
3. Le texte est prétraité, avec une attention particulière à la segmentation en paragraphes et à l'identification des en-têtes/pieds de page.
4. Le texte préparé est traduit.
5. Le fichier texte traduit est reconstitué en préservant la structure originale.

Ces architectures illustrent notre approche approfondie de la traduction, en tenant compte des spécificités de chaque type de média pour assurer des résultats de haute qualité, particulièrement adaptés aux nuances du darija marocain.

## 🚀 Mise en route rapide


1. Clonez le dépôt :
   ```
   git clone https://github.com/votre-nom-utilisateur/traducteur-multimedia.git
   cd traducteur-multimedia
   ```

2. Configurez l'environnement :
   ```
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Lancez l'application :
   ```
   streamlit run interface.py
   ```

4. Pour l'API (optionnel) :
   ```
   uvicorn api:app --reload
   ```

## 🔮 Vision future

Nous aspirons à continuellement améliorer et étendre notre plateforme :

- Intégration de plus de dialectes régionaux marocains
- Développement de modèles de traduction spécifiques à divers domaines (médical, juridique, technique)
- Implémentation de la traduction en temps réel pour les appels vidéo et les conférences
- Création d'outils éducatifs basés sur l'IA pour l'apprentissage du darija

## 🤝 Contribuer au projet

Nous accueillons chaleureusement les contributions ! Pour participer :

1. Forkez le projet
2. Créez votre branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request
## Démonstration

Pour voir l'application en action, consultez notre vidéo de démonstration :

🎥 [Regarder la démo sur YouTube](https://youtu.be/gAaMFbuXZP4?si=xaCsyITjToyP41EzJ)
## 📜 Licence

Ce projet est distribué sous la licence MIT. Consultez le fichier `LICENSE` pour plus de détails.

## 📬 Contact et support

Yahya Zakariae - zakariae.yh@gmail.com

Lien du projet : [https://github.com/votre-nom-utilisateur/traducteur-multimedia](https://github.com/zakariaeyahya/Plateforme_Web_de_Traduction_Multim-dia_Intelligente.git)

## 🙏 Remerciements

Un grand merci à la communauté open-source et aux créateurs des technologies qui rendent ce projet possible 

---

Développé avec passion et dédication par Yahya Zakariae 🚀
