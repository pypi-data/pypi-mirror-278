import os
import streamlit.components.v1 as components

_DEVELOPMENT = False

if _DEVELOPMENT:
    _component_func = components.declare_component(
        "st_audio_spectrogram",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        "st_audio_spectrogram",
        path=build_dir
    )


def st_audio_spectrogram(data, key=None):
    return _component_func(data=data, key=key, default=0)
