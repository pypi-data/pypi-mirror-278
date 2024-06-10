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

def get_colormap_names():
    """
    Get a list of color maps for spectrogram.
    """
    return [
        "alpha",
        "autumn",
        "bathymetry",
        "blackbody",
        "bluered",
        "bone",
        "cdom",
        "chlorophyll",
        "cool",
        "copper",
        "cubehelix",
        "density",
        "earth",
        "electric",
        "freesurface-blue",
        "freesurface-red",
        "greens",
        "greys",
        "hot",
        "hsv",
        "inferno",
        "jet",
        "magma",
        "oxygen",
        "par",
        "phase",
        "picnic",
        "plasma",
        "portland",
        "rainbow",
        "rainbow-soft",
        "rdbu",
        "salinity",
        "spring",
        "summer",
        "temperature",
        "turbidity",
        "velocity-blue",
        "velocity-green",
        "viridis",
        "warm",
        "winter",
        "yignbu",
        "yiorrd",
    ]

def get_default_config():
    """
    Get the default settings for the component.
    """
    return {
        "cursor": {
            "color": "blue",
            "width": 4,
        },
        "waveform": {
            "height": 128,
            "color": "#4F4A85",
            "progressColor": '#383351',
            "normalize": True,
        },
        "spectrogram": {
            "height": 128,
            "labels": True,
        },
        "colormap": {
            "colormap": "plasma",
            "nshades": 256,
            "format": "float",
        },
        "mediaControls": True,
    }

def st_audio_spectrogram(data, config=None, key=None):
    """
    Create an Audio/Spectrogram visualization.
    """
    audio_config = get_default_config()
    if config:
        audio_config.update(config)

    if audio_config["colormap"]["colormap"] not in get_colormap_names():
        raise Exception("Unknown colormap name: %r" % audio_config["colormap"]["colormap"])

    return _component_func(data=data, config=audio_config, key=key, default=0)
