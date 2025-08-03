import streamlit as st
from googletrans import Translator
from gtts import gTTS
import base64
import os


st.set_page_config(
    page_title="LanG-TransO",
    page_icon="logo.png",  # You can use an emoji or a URL to an image
    layout="centered"
)
# --- Page Config ---
st.set_page_config(page_title="AI Translator", layout="centered")

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
st.subheader("📝 Enter Text to Translate")
input_text = st.text_area("", height=150)

# --- Language Selection ---
col1, col2 = st.columns(2)
with col1:
    auto_detect = st.checkbox("🌐 Auto Detect Input Language", value=True)
    if not auto_detect:
        input_lang = st.selectbox("From Language", options=languages.keys(), index=0)
    else:
        input_lang = None
with col2:
    output_lang = st.selectbox("🎯 To Language", options=languages.keys(), index=1)

# --- Translate Button ---
if st.button("🚀 Translate"):
    if input_text.strip() == "":
        st.warning("⚠️ Please enter some text.")
    else:
        translator = Translator()

        if auto_detect:
            detected = translator.detect(input_text)
            detected_lang_code = detected.lang
            detected_lang_name = next((k for k, v in languages.items() if v == detected_lang_code), detected_lang_code)
            st.info(f"🔍 Detected Language: **{detected_lang_name.title()}** (`{detected_lang_code}`)")
        else:
            detected_lang_code = languages[input_lang]

        translated = translator.translate(input_text, src=detected_lang_code, dest=languages[output_lang])

        st.subheader("📄 Translated Output")
        st.text_area("", translated.text, height=150)

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
