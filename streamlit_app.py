import os
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from signal_generator import (
    create_time_vector,
    create_sinc_time_vector,
    generate_sine,
    generate_cosine,
    generate_square,
    generate_triangle,
    generate_sinc,
    generate_chirp
)

from analyzer import calculate_fft, calculate_stft
from audio import (
    save_audio,
    load_audio,
    play_audio,
    stop_audio,
    record_audio
)
# -------------------------------
# Page configuration
# -------------------------------

st.set_page_config(
    page_title="SP24 Signal Generator",
    page_icon="🎵",
    layout="wide"
)


# -------------------------------
# Title
# -------------------------------

st.title("🎵 SP24 Signal Generator and Analyzer")

st.write(
    "Generate different audio-range signals and visualize "
    "their waveforms."
)


# -------------------------------
# Sidebar
# -------------------------------

st.sidebar.header("Signal Parameters")


signal_type = st.sidebar.selectbox(
    "Select Signal",
    [
        "Sine",
        "Cosine",
        "Square",
        "Triangle",
        "Sinc",
        "Chirp"
    ]
)


if signal_type != "Chirp":

    frequency = st.sidebar.number_input(
        "Frequency (Hz)",
        min_value=1.0,
        value=440.0
    )

else:

    frequency = 0.0


amplitude = st.sidebar.number_input(
    "Amplitude",
    min_value=0.0,
    value=1.0
)


duration = st.sidebar.number_input(
    "Duration (seconds)",
    min_value=0.01,
    value=2.0
)


sample_rate = st.sidebar.number_input(
    "Sampling Rate (Hz)",
    min_value=100.0,
    value=44100.0
)


# ------------------------------
# Additional parameters
# -------#------------------------

duty_cycle = 50

if signal_type == "Square":

    duty_cycle = st.sidebar.slider(
        "Duty Cycle (%)",
        min_value=1,
        max_value=99,
        value=50
    )


# Chirp parameters

start_frequency = 0.0
end_frequency = 0.0

if signal_type == "Chirp":

    start_frequency = st.sidebar.number_input(
        "Start Frequency (Hz)",
        min_value=1.0,
        value=100.0
    )

    end_frequency = st.sidebar.number_input(
        "End Frequency (Hz)",
        min_value=1.0,
        value=1000.0
    )


# Phase

phase = 0

if signal_type in ["Sine", "Cosine"]:

    phase = st.sidebar.number_input(
        "Phase (degrees)",
        min_value=0.0,
        max_value=360.0,
        value=0.0
    )


# -------------------------------
# Generate button
# -------------------------------

generate_button = st.button(
    "⚡ Generate Signal"
)


# -------------------------------
# Generate signal
# -------------------------------

if generate_button:

    # Create time vector

    if signal_type == "Sinc":

        t = create_sinc_time_vector(
            duration,
            sample_rate
        )

    else:

        t = create_time_vector(
            duration,
            sample_rate
        )


    # Generate selected signal

    if signal_type == "Sine":

        y = generate_sine(
            t,
            frequency,
            amplitude,
            phase
        )


    elif signal_type == "Cosine":

        y = generate_cosine(
            t,
            frequency,
            amplitude,
            phase
        )


    elif signal_type == "Square":

        y = generate_square(
            t,
            frequency,
            amplitude,
            duty_cycle
        )


    elif signal_type == "Triangle":

        y = generate_triangle(
            t,
            frequency,
            amplitude
        )


    elif signal_type == "Sinc":

        y = generate_sinc(
            t,
            frequency,
            amplitude
        )


    elif signal_type == "Chirp":

        y = generate_chirp(
            t,
            start_frequency,
            end_frequency,
            duration,
            amplitude
        )


    # -------------------------------
    # Save signal in Streamlit memory
    # -------------------------------

    st.session_state["time"] = t
    st.session_state["signal"] = y
    st.session_state["sample_rate"] = sample_rate
    st.session_state["signal_type"] = signal_type


# -------------------------------
# Display waveform
# -------------------------------

if "signal" in st.session_state:

    t = st.session_state["time"]
    y = st.session_state["signal"]
    sample_rate = st.session_state["sample_rate"]
    signal_type = st.session_state["signal_type"]


    st.success(
        f"{signal_type} signal generated successfully!"
    )


    st.subheader("Time Domain Waveform")
    

    fig, ax = plt.subplots(figsize=(10, 4))


    # Display Sinc around its center
    # Display Sinc around its center
    if signal_type == "Sinc":

        center = len(t) // 2
        half_window = min(2500, center)

        start = center - half_window
        end = center + half_window

        ax.plot(
            t[start:end],
            y[start:end]
        )

    else:

        # Don't display millions of points
        display_points = min(len(t), 5000)

        ax.plot(
            t[:display_points],
            y[:display_points]
        )

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title(
        f"{signal_type} Signal"
    )

    ax.grid(True)

    st.pyplot(fig)

    plt.close(fig)

    # -------------------------------
# FFT Analysis
# -------------------------------
    # -------------------------------
    # FFT Analysis
    # -------------------------------

    st.subheader("📊 FFT Spectrum")

    frequencies, magnitude = calculate_fft(
        y,
        sample_rate
    )

    fig_fft, ax_fft = plt.subplots(
        figsize=(10, 4)
    )

    ax_fft.plot(
        frequencies,
        magnitude
    )
    ax_fft.set_xlim(
        0,    
       min(sample_rate / 2, 5000)
    )


    ax_fft.set_xlabel("Frequency (Hz)")
    ax_fft.set_ylabel("Magnitude")
    ax_fft.set_title("FFT Spectrum")
    ax_fft.grid(True)

    st.pyplot(fig_fft)

    plt.close(fig_fft)


# -------------------------------
# STFT Analysis
# -------------------------------
    # -------------------------------
    # STFT Analysis
    # -------------------------------

    st.subheader("🌈 STFT Spectrogram")

    stft_frequencies, stft_times, stft_magnitude = calculate_stft(
        y,
        sample_rate
    )

    fig_stft, ax_stft = plt.subplots(
        figsize=(10, 5)
    )

    mesh = ax_stft.pcolormesh(
        stft_times,
        stft_frequencies,
        stft_magnitude,
        shading="gouraud"
    )

    ax_stft.set_xlabel("Time (s)")
    ax_stft.set_ylabel("Frequency (Hz)")
    ax_stft.set_title("STFT Spectrogram")
    ax_stft.set_ylim(
        0,
        min(sample_rate / 2, 5000)
    )
    fig_stft.colorbar(
        mesh,
        ax=ax_stft,
        label="Magnitude"
    )

    st.pyplot(fig_stft)

    plt.close(fig_stft)


    # Signal information

    # -------------------------------
# Signal Information
# -------------------------------
# -------------------------------
# Signal Information
# -------------------------------

if "signal" in st.session_state:

    current_signal = st.session_state["signal"]

    st.subheader("Signal Information")

    if signal_type == "Chirp":

        chirp_rate = (
            end_frequency - start_frequency
        ) / duration

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        col1.metric(
            "Signal",
            signal_type
        )

        col2.metric(
            "Start Frequency",
            f"{start_frequency} Hz"
        )

        col3.metric(
            "End Frequency",
            f"{end_frequency} Hz"
        )

        col4.metric(
            "Chirp Rate",
            f"{chirp_rate:.1f} Hz/s"
        )

        col5.metric(
            "Amplitude",
            amplitude
        )

        col6.metric(
            "Samples",
            len(current_signal)
        )

    else:

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Signal",
            signal_type
        )

        col2.metric(
            "Frequency",
            f"{frequency} Hz"
        )

        col3.metric(
            "Amplitude",
            amplitude
        )

        col4.metric(
            "Samples",
            len(current_signal)
        )
    # -------------------------------
    # Audio Controls
    # -------------------------------

    st.subheader("🎵 Audio Controls")

    audio_col1, audio_col2, audio_col3 = st.columns(3)

    with audio_col1:
        if st.button("▶ Play Signal"):
            play_audio(y, int(sample_rate))
            st.success("Playback started!")

    with audio_col2:
        if st.button("⏹ Stop Signal"):
            stop_audio()
            st.info("Playback stopped.")

    with audio_col3:
        if st.button("💾 Save WAV"):
            filename = f"{signal_type.lower()}_signal.wav"

            save_audio(
                filename,
                y,
                int(sample_rate)
            )

            filepath = os.path.join(
                "generated",
                "audio",
                filename
            )

            with open(filepath, "rb") as audio_file:
                st.download_button(
                    label="⬇️ Download WAV",
                    data=audio_file,
                    file_name=filename,
                    mime="audio/wav"
                )
# -------------------------------
# Load WAV File
# -------------------------------

st.subheader("📂 Load WAV File")

uploaded_file = st.file_uploader(
    "Upload a WAV audio file",
    type=["wav"]
)

if uploaded_file is not None:

    # Save uploaded file temporarily
    temp_filename = "uploaded_audio.wav"

    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())

    loaded_sample_rate, loaded_signal = load_audio(
        temp_filename
    )

    st.success("WAV file loaded successfully!")

    # Store loaded audio
    st.session_state["loaded_signal"] = loaded_signal
    st.session_state["loaded_sample_rate"] = loaded_sample_rate              
# -------------------------------
# Analyze Loaded WAV
# -------------------------------

if "loaded_signal" in st.session_state:

    loaded_signal = st.session_state["loaded_signal"]
    loaded_sample_rate = st.session_state["loaded_sample_rate"]

    st.subheader("📈 Loaded WAV Analysis")

    # Create time vector
    loaded_time = (
    np.arange(len(loaded_signal))
    / loaded_sample_rate
   )

    # -------------------------------
# Time Domain
# ------------------------------
     # -------------------------------
# Time Domain
# -------------------------------

    st.write("### Time Domain Waveform")

    fig_loaded, ax_loaded = plt.subplots(
       figsize=(10, 4)
    )

    if signal_type == "Sinc":

        center = len(loaded_signal) // 2
        half_window = min(2500, center)

        start = center - half_window
        end = center + half_window

        sinc_time = (
            np.arange(start, end) - center
        ) / loaded_sample_rate

        ax_loaded.plot(
        sinc_time,
        loaded_signal[start:end]
        )

    else:

       display_points = min(
          len(loaded_signal),
          5000
        )

       ax_loaded.plot(
          loaded_time[:display_points],
          loaded_signal[:display_points]
        )

    ax_loaded.set_xlabel("Time (s)")
    ax_loaded.set_ylabel("Amplitude")
    ax_loaded.set_title("Loaded WAV Signal")
    ax_loaded.grid(True)

    st.pyplot(fig_loaded)

    plt.close(fig_loaded)

    # -------------------------------
    # FFT
    # -------------------------------

    st.write("### 📊 FFT Spectrum")

    loaded_frequencies, loaded_magnitude = calculate_fft(
        loaded_signal,
        loaded_sample_rate
    )

    fig_loaded_fft, ax_loaded_fft = plt.subplots(
        figsize=(10, 4)
    )

    ax_loaded_fft.plot(
        loaded_frequencies,
        loaded_magnitude
    )
    # Limit displayed frequency range
    ax_loaded_fft.set_xlim(
        0,
        min(loaded_sample_rate / 2, 5000)
    )

    ax_loaded_fft.set_xlabel("Frequency (Hz)")
    ax_loaded_fft.set_ylabel("Magnitude")
    ax_loaded_fft.set_title("FFT of Loaded WAV")
    ax_loaded_fft.grid(True)

    st.pyplot(fig_loaded_fft)

    plt.close(fig_loaded_fft)

    # -------------------------------
    # STFT
    # -------------------------------

    st.write("### 🌈 STFT Spectrogram")

    loaded_stft_frequencies, loaded_stft_times, loaded_stft_magnitude = calculate_stft(
        loaded_signal,
        loaded_sample_rate
    )

    fig_loaded_stft, ax_loaded_stft = plt.subplots(
        figsize=(10, 5)
    )

    mesh_loaded = ax_loaded_stft.pcolormesh(
        loaded_stft_times,
        loaded_stft_frequencies,
        loaded_stft_magnitude,
        shading="gouraud"
    )

    ax_loaded_stft.set_xlabel("Time (s)")
    ax_loaded_stft.set_ylabel("Frequency (Hz)")
    ax_loaded_stft.set_title("STFT of Loaded WAV")
    ax_loaded_stft.set_ylim(
        0,
        min(loaded_sample_rate / 2, 5000)
    )


    fig_loaded_stft.colorbar(
        mesh_loaded,
        ax=ax_loaded_stft,
        label="Magnitude"
    )

    st.pyplot(fig_loaded_stft)

    plt.close(fig_loaded_stft)  

  # -------------------------------
# Record Audio
# -------------------------------

st.subheader("🎙 Record Audio")

record_duration = st.number_input(
    "Recording Duration (seconds)",
    min_value=1.0,
    max_value=30.0,
    value=5.0
)

if st.button("🎙 Start Recording"):

    st.info("Recording... Please speak into your microphone.")

    recorded_signal = record_audio(
        record_duration,
        int(sample_rate)
    )

    st.session_state["recorded_signal"] = recorded_signal
    st.session_state["recorded_sample_rate"] = int(sample_rate)

    st.success("Recording completed successfully!")


# -------------------------------
# Analyze Recorded Audio
# -------------------------------

if "recorded_signal" in st.session_state:

    recorded_signal = st.session_state["recorded_signal"]
    recorded_sample_rate = st.session_state["recorded_sample_rate"]

    st.subheader("📈 Recorded Audio Analysis")

    # Create time vector

    recorded_time = (
        np.arange(len(recorded_signal))
        / recorded_sample_rate
    )

    # -------------------------------
    # Time Domain
    # -------------------------------

    st.write("### Time Domain Waveform")

    fig_record, ax_record = plt.subplots(
        figsize=(10, 4)
    )

    display_points = min(
        len(recorded_signal),
        5000
    )

    ax_record.plot(
        recorded_time[:display_points],
        recorded_signal[:display_points]
    )

    ax_record.set_xlabel("Time (s)")
    ax_record.set_ylabel("Amplitude")
    ax_record.set_title("Recorded Audio")
    ax_record.grid(True)

    st.pyplot(fig_record)

    plt.close(fig_record)

    # -------------------------------
    # FFT
    # -------------------------------

    st.write("### 📊 FFT Spectrum")

    recorded_frequencies, recorded_magnitude = calculate_fft(
        recorded_signal,
        recorded_sample_rate
    )

    fig_record_fft, ax_record_fft = plt.subplots(
        figsize=(10, 4)
    )

    ax_record_fft.plot(
        recorded_frequencies,
        recorded_magnitude
    )

    ax_record_fft.set_xlabel("Frequency (Hz)")
    ax_record_fft.set_ylabel("Magnitude")
    ax_record_fft.set_title("FFT of Recorded Audio")
    ax_record_fft.grid(True)

    st.pyplot(fig_record_fft)

    plt.close(fig_record_fft)

    # -------------------------------
    # STFT
    # -------------------------------

    st.write("### 🌈 STFT Spectrogram")

    recorded_stft_frequencies, recorded_stft_times, recorded_stft_magnitude = calculate_stft(
        recorded_signal,
        recorded_sample_rate
    )

    fig_record_stft, ax_record_stft = plt.subplots(
        figsize=(10, 5)
    )

    mesh_record = ax_record_stft.pcolormesh(
        recorded_stft_times,
        recorded_stft_frequencies,
        recorded_stft_magnitude,
        shading="gouraud"
    )

    ax_record_stft.set_xlabel("Time (s)")
    ax_record_stft.set_ylabel("Frequency (Hz)")
    ax_record_stft.set_title("STFT of Recorded Audio")

    fig_record_stft.colorbar(
        mesh_record,
        ax=ax_record_stft,
        label="Magnitude"
    )

    st.pyplot(fig_record_stft)

    plt.close(fig_record_stft)
 # -------------------------------
# Recorded Audio Controls
# -------------------------------

if "recorded_signal" in st.session_state:

    st.subheader("🎵 Recorded Audio Controls")

    record_col1, record_col2, record_col3 = st.columns(3)

    # Play
    with record_col1:

        if st.button("▶ Play Recording"):

            play_audio(
                st.session_state["recorded_signal"],
                st.session_state["recorded_sample_rate"]
            )

            st.success("Recorded audio playback started!")

    # Stop
    with record_col2:

        if st.button("⏹ Stop Recording"):

            stop_audio()

            st.info("Playback stopped.")

    # Save
    with record_col3:

        if st.button("💾 Save Recording"):

            save_audio(
                "recorded_audio.wav",
                st.session_state["recorded_signal"],
                st.session_state["recorded_sample_rate"]
            )

            st.success("Recording saved successfully!")

            filepath = os.path.join(
                "generated",
                "audio",
                "recorded_audio.wav"
            )

            with open(filepath, "rb") as audio_file:

                st.download_button(
                    label="⬇️ Download Recording",
                    data=audio_file,
                    file_name="recorded_audio.wav",
                    mime="audio/wav"
                )   