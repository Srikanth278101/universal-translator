import streamlit as st
from audio_recorder_streamlit import audio_recorder
from deep_translator import GoogleTranslator
from gtts import gTTS
import asyncio
import edge_tts
import os
import time

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

# భాషల లిస్ట్ (సరిచేసిన సింటాక్స్ తో)
languages = {
    "Telugu (తెలుగు)": {"code": "te", "tts_method": "gtts", "tts_code": "te"},
    "English": {"code": "en", "tts_method": "gtts", "tts_code": "en"},
    "Tamil (தமிழ்)": {"code": "ta", "tts_method": "gtts", "tts_code": "ta"},
    "Hindi (हिन्दी)": {"code": "hi", "tts_method": "gtts", "tts_code": "hi"},
    "Odia (ଓଡ଼ିଆ)": {"code": "or", "tts_method": "edge", "tts_code": "or-IN-SubhasiniNeural"},
    "Kannada (ಕನ್ನಡ)": {"code": "kn", "tts_method": "gtts", "tts_code": "kn"},
    "Malayalam (മലയാളం)": {"code": "ml", "tts_method": "gtts", "tts_code": "ml"},
    "Marathi (మరాठी)": {"code": "mr", "tts_method": "gtts", "tts_code": "mr"},
    "Bengali (বাংলা)": {"code": "bn", "tts_method": "gtts", "tts_code": "bn"},
    "French": {"code": "fr", "tts_method": "gtts", "tts_code": "fr"},
    "Japanese": {"code": "ja", "tts_method": "gtts", "tts_code": "ja"},  # ఇక్కడ కామా పెట్టాం
    "Chinese (Mandarin)": {"code": "zh-CN", "tts_method": "gtts", "tts_code": "zh-CN"},
    "Russian (రష్యన్)": {"code": "ru", "tts_method": "gtts", "tts_code": "ru"},
    "Ukrainian (ఉక్రేనియన్)": {"code": "uk", "tts_method": "gtts", "tts_code": "uk"},
    "Mongolian (మంగోలియన్)": {"code": "mn", "tts_method": "gtts", "tts_code": "mn"},
    "Korean (కొరియన్)": {"code": "ko", "tts_method": "gtts", "tts_code": "ko"}
} # ఇక్కడ ఎక్స్‌ట్రా బ్రాకెట్ తీసేశాం

col_lang1, col_lang2 = st.columns(2)
with col_lang1:
    my_lang = st.selectbox("🙋‍♂️ నీ భాష (Your Language):", list(languages.keys()), index=0)
with col_lang2:
    tour_lang = st.selectbox("🗺️ ప్రాంతీయ భాష (Local Language):", list(languages.keys()), index=1)

lang1_data = languages[my_lang]
lang2_data = languages[tour_lang]

st.write("---")

async def amake_edge_tts(text, voice_name, output_file):
    communicate = edge_tts.Communicate(text, voice_name)
    await communicate.save(output_file)

st.write("### ✍️ Type or Use Voice Typing")
user_input = st.text_input(f"{my_lang} లో ఇక్కడ రాయండి (లేదా కీబోర్డ్ మైక్ వాడండి):", key="user_text_input")

if st.button("🔄 Translate (అనువదించు)", use_container_width=True, type="primary"):
    if user_input:
        with st.spinner("అనువదిస్తోంది..."):
            try:
                # 1. అనువాదం
                translated = GoogleTranslator(source=lang1_data["code"], target=lang2_data["code"]).translate(user_input)
                
                # స్క్రీన్ పై టెక్స్ట్ చూపించడం
                st.markdown(f"<div class='user-box'><b>నువ్వు చెప్పింది:</b><br>{user_input}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='reply-box'><b>అనువాదం ({tour_lang}):</b><br>{translated}</div>", unsafe_allow_html=True)
                
                # 2. ప్రతిసారీ కొత్త ఆడియో ఫైల్ క్రియేట్ చేయడం
                unique_id = int(time.time())
                out_filename = f"trans_out_{unique_id}.mp3"
                
                try:
                    if lang2_data["tts_method"] == "edge":
                        asyncio.run(amake_edge_tts(translated, lang2_data["tts_code"], out_filename))
                    else:
                        tts = gTTS(text=translated, lang=lang2_data["tts_code"])
                        tts.save(out_filename)
                    
                    # ఆడియో ప్లే చేయడం
                    st.audio(out_filename, format="audio/mp3", autoplay=True)
                    
                except Exception as audio_err:
                    st.warning("ఈ భాషకి ఆడియో ప్లే చేయడంలో చిన్న సమస్య వచ్చింది. పైన టెక్స్ట్ చూడవచ్చు.")
                    
            except Exception as e:
                st.error(f"అనువాదంలో సమస్య వచ్చింది: {e}")
    else:
        st.warning("⚠️ ముందు పైన ఉన్న బాక్స్ లో ఏదైనా టైప్ చేయండి!")

st.write("---")
st.write("### 🎤 Direct Audio Recorder (Beta)")
audio_bytes = audio_recorder(text="క్లిక్ చేసి మాట్లాడండి", recording_color="#e74c3c", neutral_color="#95a5a6")
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
