import streamlit as st
from audio_recorder_streamlit import audio_recorder
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

# మొబైల్ వ్యూ సెట్టింగ్స్
st.set_page_config(page_title="Universal Tour Translator", page_icon="✈️", layout="centered")

st.markdown("""
    <style>
    .title { text-align: center; color: #FF4B4B; font-size: 30px; font-weight: bold; }
    .user-box { background-color: #E8F0FE; padding: 15px; border-radius: 10px; margin-bottom: 10px; color: #1A73E8; }
    .reply-box { background-color: #E6F4EA; padding: 15px; border-radius: 10px; margin-bottom: 10px; color: #137333; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="title">✈️ Universal Tour Translator</p>', unsafe_allow_html=True)
st.write("---")

# సపోర్ట్ చేసే భాషల లిస్ట్ (Odia యాడ్ చేయబడింది)
languages = {
    "Telugu (తెలుగు)": {"code": "te", "tts_code": "te"},
    "English": {"code": "en", "tts_code": "en"},
    "Tamil (தமிழ்)": {"code": "ta", "tts_code": "ta"},
    "Hindi (हिन्दी)": {"code": "hi", "tts_code": "hi"},
    "Odia (ଓଡ଼ିଆ)": {"code": "or", "tts_code": "or"},  # <-- ఓడియా లాంగ్వేజ్ కోడ్
    "Kannada (ಕನ್ನಡ)": {"code": "kn", "tts_code": "kn"},
    "Malayalam (മലയാളം)": {"code": "ml", "tts_code": "ml"},
    "Marathi (मराठी)": {"code": "mr", "tts_code": "mr"},
    "Bengali (বাংলা)": {"code": "bn", "tts_code": "bn"},
    "French": {"code": "fr", "tts_code": "fr"},
    "Japanese": {"code": "ja", "tts_code": "ja"}
}

col_lang1, col_lang2 = st.columns(2)
with col_lang1:
    my_lang = st.selectbox("🙋‍♂️ నీ భాష (Your Language):", list(languages.keys()), index=0)
with col_lang2:
    tour_lang = st.selectbox("🗺️ ప్రాంతీయ భాష (Local Language):", list(languages.keys()), index=1)

lang1_data = languages[my_lang]
lang2_data = languages[tour_lang]

# టెక్స్ట్ బేస్డ్ ట్రాన్స్లేషన్
st.write("### ✍️ Type or Use Voice Typing")
user_input = st.text_input(f"{my_lang} లో ఇక్కడ రాయండి (లేదా కీబోర్డ్ మైక్ వాడండి):")

if user_input:
    translated = GoogleTranslator(source=lang1_data["code"], target=lang2_data["code"]).translate(user_input)
    st.markdown(f"<div class='reply-box'><b>అనువాదం ({tour_lang}):</b><br>{translated}</div>", unsafe_allow_html=True)
    
    # ఆడియో ప్లే చేయడం
    tts = gTTS(text=translated, lang=lang2_data["tts_code"])
    tts.save("trans_out.mp3")
    st.audio("trans_out.mp3", format="audio/mp3", autoplay=True)

st.write("---")
st.write("### 🎤 Direct Audio Recorder (Beta)")
st.write("కింది మైక్ గుర్తుపై క్లిక్ చేసి మాట్లాడండి:")

audio_bytes = audio_recorder(text="క్లిక్ చేసి మాట్లాడండి", recording_color="#e74c3c", neutral_color="#95a5a6")

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    st.info("గమనిక: మొబైల్ బ్రౌజర్ లలో కీబోర్డ్ మైక్ ఆప్షన్ మోర్ రిలయబుల్ గా పనిచేస్తుంది.")
