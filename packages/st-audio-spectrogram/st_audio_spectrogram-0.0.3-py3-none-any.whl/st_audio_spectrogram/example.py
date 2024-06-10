import streamlit as st
import os
from st_audio_spectrogram import st_audio_spectrogram

HERE = os.path.dirname(os.path.abspath(__file__))

filename = os.path.join(HERE, "frontend/public/demo.wav")
data = open(filename, "rb").read()

config = {
    "colormap": {
        "colormap": "autumn",
    },
}

st_audio_spectrogram(data, config) # .decode('utf-8'))
