import streamlit as st
import googletrans
import speech_recognition as sr
import gtts
import tempfile
import os

# Set the page title and description
st.header("Project of PGD Batch 5")
st.subheader("Submitted by Gul Zaman")
st.write("Submitted to Sir Muhammad Qasim")
st.title("Speech Translation App")
st.write("Select a translation option and language:")

# List of supported languages
languages = googletrans.LANGUAGES
language_codes = list(languages.keys())
language_names = list(languages.values())

# Initialize Streamlit UI
st.sidebar.header("Translation Options")
translation_option = st.sidebar.radio("Select a Translation Option:", ["Speech to Speech", "Speech to Text", "Text to Text", "Text to Speech"])

# Language selection
select_language_index = st.selectbox("Select Language for Translation:", language_names)
select_language = language_codes[language_names.index(select_language_index)]

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Function for Speech to Speech Translation
def translate_speech_to_speech():
    st.info("Click the 'Translate' button to start translation.")
    
    if st.button("Translate"):
        try:
            with sr.Microphone() as source:
                st.info("Listening for speech...")
                audio = recognizer.listen(source, timeout=10)
                detected_language = recognizer.recognize_google(audio, language="en")
                st.info(f"Detected Text: {detected_language}")
            st.success("Translating.....")

            translator = googletrans.Translator()
            detected_language_code = translator.detect(detected_language).lang
            translated_text = translator.translate(recognizer.recognize_google(audio, language=detected_language_code), dest=select_language)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                temp_audio_path = temp_audio.name
                gtts.gTTS(translated_text.text, lang=select_language).save(temp_audio_path)

            # Play the translated audio
            st.audio(open(temp_audio_path, 'rb').read(), format="audio/mp3")
            os.remove(temp_audio_path)  # Remove temporary audio file
        except sr.WaitTimeoutError:
            st.warning("No speech detected. Please try again.")
        except sr.RequestError:
            st.error("Sorry, an error occurred while processing your request.")

# Function for Speech to Text Translation
def translate_speech_to_text():
    st.info("Click the 'Translate' button to start translation.")
    
    if st.button("Translate"):
        try:
            with sr.Microphone() as source:
                st.info("Listening for speech...")
                audio = recognizer.listen(source, timeout=10)
                detected_language = recognizer.recognize_google(audio, language="en")
                st.info(f"Detected Text: {detected_language}")
            st.success("Translating.....")

            translator = googletrans.Translator()
            detected_language_code = translator.detect(detected_language).lang
            translated_text = translator.translate(recognizer.recognize_google(audio, language=detected_language_code), dest=select_language)
            
            # Display the translated text
            st.subheader(f"Translated Text ({select_language_index}):")
            st.text_area("Translated Text:", translated_text.text)
        except sr.WaitTimeoutError:
            st.warning("No speech detected. Please try again.")
        except sr.RequestError:
            st.error("Sorry, an error occurred while processing your request.")

# Function for Text to Text Translation
def translate_text_to_text():
    text_input = st.text_area("Enter the text you want to translate:")

    if st.button("Translate"):
        if text_input:
            translator = googletrans.Translator()
            translation = translator.translate(text_input, dest=select_language)
            
            # Display the translated text
            st.subheader(f"Translated Text ({select_language_index}):")
            st.text_area("Translated Text:", translation.text)

# Function for Text to Speech Translation
def translate_text_to_speech():
    text_input = st.text_area("Enter the text you want to translate:")

    if st.button("Translate"):
        if text_input:
            translator = googletrans.Translator()
            translation = translator.translate(text_input, dest=select_language)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                temp_audio_path = temp_audio.name
                gtts.gTTS(translation.text, lang=select_language).save(temp_audio_path)

            # Play the translated audio
            st.audio(open(temp_audio_path, 'rb').read(), format="audio/mp3")
            os.remove(temp_audio_path)  # Remove temporary audio file

            # Display the translated text
            st.subheader(f"Translated Text ({select_language_index}):")
            st.text_area("Translated Text", translation.text)

# Call the appropriate translation function based on the selected option
if translation_option == "Speech to Speech":
    translate_speech_to_speech()
elif translation_option == "Speech to Text":
    translate_speech_to_text()
elif translation_option == "Text to Text":
    translate_text_to_text()
elif translation_option == "Text to Speech":
    translate_text_to_speech()
