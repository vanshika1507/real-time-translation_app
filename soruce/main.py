import os
import time
import pygame
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from googletrans import LANGUAGES, Translator

# Set page config for better display
st.set_page_config(page_title="Real-Time Language Translator", layout="wide")

# Custom CSS to improve aesthetics with light pink and light blue and background image
st.markdown("""
    <style>
        body {
            background-image: url("https://drive.google.com/file/d/1_WbEXqymRLk1-F75h8pCfvoK9jDcYebK/view?usp=sharing"); /* Replace with your image URL */
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        .stButton button {
            background-color: #FFB6C1;  /* Light pink */
            color: white;
            border-radius: 12px;
            font-size: 16px;
            padding: 10px 24px;
            margin-top: 20px;
            margin-bottom: 20px;
        }

        .stButton button:hover {
            background-color: #87CEFA; /* Light blue on hover */
        }

        .stTitle {
            color: #333333;
            font-size: 40px;
            text-align: center;
            font-family: 'Arial', sans-serif;
        }

        .stSelectbox label {
            font-size: 18px;
            color: #555;
        }

        .stSelectbox div {
            font-size: 16px;
            color: #333;
        }

        .output-placeholder {
            color: #1f77b4;
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
            background-color: #f0f8ff;
            border-radius: 5px;
            text-align: center;
        }

        .stSidebar {
            background-color: #f4f4f4;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize necessary modules
isTranslateOn = False
translator = Translator()  # Initialize the translator module
pygame.mixer.init()  # Initialize the mixer module

# Create a mapping between language names and language codes
language_mapping = {name: code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)

def translator_function(spoken_text, from_language, to_language):
    return translator.translate(spoken_text, src=from_language, dest=to_language)

def text_to_voice(text_data, to_language):
    myobj = gTTS(text=text_data, lang=to_language, slow=False)
    myobj.save("cache_file.mp3")
    audio = pygame.mixer.Sound("cache_file.mp3")
    audio.play()
    os.remove("cache_file.mp3")

def main_process(output_placeholder, from_language, to_language):
    global isTranslateOn
    while isTranslateOn:
        rec = sr.Recognizer()
        with sr.Microphone() as source:
            output_placeholder.markdown('<div class="output-placeholder">Listening...</div>', unsafe_allow_html=True)
            rec.pause_threshold = 1
            audio = rec.listen(source, phrase_time_limit=10)

        try:
            output_placeholder.markdown('<div class="output-placeholder">Processing...</div>', unsafe_allow_html=True)
            spoken_text = rec.recognize_google(audio, language=from_language)

            output_placeholder.markdown('<div class="output-placeholder">Translating...</div>', unsafe_allow_html=True)
            translated_text = translator_function(spoken_text, from_language, to_language)

            text_to_voice(translated_text.text, to_language)

        except Exception as e:
            output_placeholder.markdown(f'<div class="output-placeholder">Error: {str(e)}</div>', unsafe_allow_html=True)

# UI layout with columns
st.markdown('<h1 class="stTitle">Real-Time Language Translator</h1>', unsafe_allow_html=True)

# Organize the UI into columns for better layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    from_language_name = st.selectbox("Select Source Language:", list(LANGUAGES.values()))
    to_language_name = st.selectbox("Select Target Language:", list(LANGUAGES.values()))

    # Convert language names to language codes
    from_language = get_language_code(from_language_name)
    to_language = get_language_code(to_language_name)

    # Start and Stop buttons with better spacing and styling
    start_button = st.button("Start Translation")
    stop_button = st.button("Stop Translation")

    output_placeholder = st.empty()

# Check if "Start" button is clicked
if start_button:
    if not isTranslateOn:
        isTranslateOn = True
        main_process(output_placeholder, from_language, to_language)

# Check if "Stop" button is clicked
if stop_button:
    isTranslateOn = False
    output_placeholder.markdown('<div class="output-placeholder">Translation stopped.</div>', unsafe_allow_html=True)
