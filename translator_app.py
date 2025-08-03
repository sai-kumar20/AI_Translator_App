import streamlit as st
from googletrans import Translator
from gtts import gTTS
import base64
import os

# --- Page Config ---
st.set_page_config(page_title="AI Translator", layout="centered")

# --- Apply Light Theme Styling ---
light_style = """
<style>
    .stApp {
        background: linear-gradient(135deg, #f0f2f6, #dfe6ec);
    }
    textarea, .stTextInput, .stSelectbox, .stButton > button {
        background-color: #ffffff;
        color: #000000;
    }
</style>
"""
st.markdown(light_style, unsafe_allow_html=True)

# --- App Title ---
st.title("🌍 AI Translator App")

# --- Language Mapping ---
languages = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Chinese": "zh-cn",
    "Arabic": "ar",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko"
}

# --- User Input ---
input_text = st.text_area("Enter Text to Translate", height=150)

# --- Language Selection ---
col1, col2 = st.columns(2)
with col1:
    auto_detect = st.checkbox("🌐 Auto Detect Input Language", value=True)
    if not auto_detect:
        input_lang = st.selectbox("From Language", options=languages.keys(), index=0)
    else:
        input_lang = None
with col2:
    output_lang = st.selectbox("To Language", options=languages.keys(), index=1)

# --- Translate ---
if st.button("Translate"):
    if input_text.strip() == "":
        st.warning("Please enter some text.")
    else:
        translator = Translator()
        
        if auto_detect:
            detected = translator.detect(input_text)
            detected_lang_code = detected.lang
            detected_lang_name = next((k for k, v in languages.items() if v == detected_lang_code), detected_lang_code)
            st.info(f"Detected Language: {detected_lang_name.title()} ({detected_lang_code})")
        else:
            detected_lang_code = languages[input_lang]

        translated = translator.translate(input_text, src=detected_lang_code, dest=languages[output_lang])
        st.text_area("Translation", translated.text, height=150)

        # --- Text-to-Speech ---
        tts = gTTS(text=translated.text, lang=languages[output_lang])
        tts.save("translated_audio.mp3")

        with open("translated_audio.mp3", "rb") as audio_file:
            audio_bytes = audio_file.read()
            b64_audio = base64.b64encode(audio_bytes).decode()

        audio_html = f"""
        <audio controls>
            <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
        </audio>
        """
        st.markdown("🔊 **Click to Hear Translation**")
        st.markdown(audio_html, unsafe_allow_html=True)

        os.remove("translated_audio.mp3")

# --- Footer ---
st.markdown("---")
