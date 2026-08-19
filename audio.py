import os
import numpy as np
from scipy.io.wavfile import write, read
import sounddevice as sd


def save_audio(filename, signal_data, sample_rate):
    max_value = np.max(np.abs(signal_data))

    if max_value > 0:
        signal_data = signal_data / max_value

    signal_data = np.int16(signal_data * 32767)

    os.makedirs("generated/audio", exist_ok=True)

    filepath = os.path.join(
        "generated/audio",
        filename
    )

    write(
        filepath,
        sample_rate,
        signal_data
    )

    print(f"Audio saved successfully: {filepath}")


def load_audio(filename):
    sample_rate, signal_data = read(filename)

    signal_data = signal_data.astype(np.float32)

    if np.max(np.abs(signal_data)) > 0:
        signal_data = signal_data / np.max(
            np.abs(signal_data)
        )

    return sample_rate, signal_data


def play_audio(signal_data, sample_rate):
    sd.play(
        signal_data,
        sample_rate
    )

    print("Audio playback started.")


def stop_audio():
    sd.stop()

    print("Audio playback stopped.")


def record_audio(duration, sample_rate):
    print("Recording started...")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    recording = recording.flatten()

    print("Recording finished.")

    return recording


if __name__ == "__main__":

    print("Testing audio.py...")
    print()

    sample_rate = 44100
    duration = 1
    frequency = 440
    amplitude = 0.5

    time = np.arange(
        0,
        duration,
        1 / sample_rate
    )

    test_signal = amplitude * np.sin(
        2 * np.pi * frequency * time
    )

    print("Test signal created.")
    print(f"Sample rate : {sample_rate} Hz")
    print(f"Duration    : {duration} second")
    print(f"Frequency   : {frequency} Hz")
    print(f"Samples     : {len(test_signal)}")
    print()

    save_audio(
        "test_audio.wav",
        test_signal,
        sample_rate
    )

    print()
    print("Testing playback...")

    play_audio(
        test_signal,
        sample_rate
    )

    sd.wait()

    print("Playback finished.")
    print()
    print("audio.py is working correctly!")