# streamlit_app.py
import os

import streamlit as st
from llm_functions import *
from app_functions import *
from st_custom_components import st_audiorec, convert_wav_to_mp3
import whisper

from llm_functions import *
from st_custom_components import convert_wav_to_mp3, st_audiorec

# Execute packages.sh on startup

## Streamlit envvars
st.write(
    "ANTHROPIC_API_KEY",
    os.environ["ANTHROPIC_API_KEY"] == st.secrets["ANTHROPIC_API_KEY"],
)
st.write(
    "OPENAI_API_KEY",
    os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"],
)
st.write(
    "ELEVENLABS_API_KEY",
    os.environ["ELEVENLABS_API_KEY"] == st.secrets["ELEVENLABS_API_KEY"],
)

WHISPER_DEFAULT_SETTINGS = {
    "whisper_model": "base",
    "temperature": 0.0,
    "temperature_increment_on_fallback": 0.2,
    "no_speech_threshold": 0.6,
    "logprob_threshold": -1.0,
    "compression_ratio_threshold": 2.4,
    "condition_on_previous_text": True,
    "verbose": False,
    "task": "transcribe",
}

## Utils
def main():
    # Set a title
    st.title("My LangChain App")

    # Select between the translation, chat, and audio recording pages
    page = st.sidebar.selectbox(
        "Choose a page:", ["Translation", "Chat", "Audio Recording", "repl agent"]
    )

    if page == "Translation":
        translation_page()
    elif page == "Chat":
        chat_page()
    elif page == "Audio Recording":
        audio_recording_page()
    elif page == "repl agent":
        repl_agent_page()


if __name__ == "__main__":
    main()
