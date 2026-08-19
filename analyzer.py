import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def calculate_fft(signal_data, sample_rate):
    n = len(signal_data)

    fft_result = np.fft.fft(signal_data)

    frequencies = np.fft.fftfreq(
        n,
        1 / sample_rate
    )

    magnitude = np.abs(fft_result) / n

    positive_frequencies = frequencies[:n // 2]
    positive_magnitude = magnitude[:n // 2]

    return positive_frequencies, positive_magnitude


def plot_fft(signal_data, sample_rate):
    frequencies, magnitude = calculate_fft(
        signal_data,
        sample_rate
    )

    plt.figure()

    plt.plot(
        frequencies,
        magnitude
    )

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("FFT Spectrum")
    plt.grid(True)

    plt.show()


def calculate_stft(signal_data, sample_rate):
    frequencies, times, stft_result = signal.stft(
        signal_data,
        fs=sample_rate
    )

    magnitude = np.abs(stft_result)

    return frequencies, times, magnitude


def plot_stft(signal_data, sample_rate):
    frequencies, times, magnitude = calculate_stft(
        signal_data,
        sample_rate
    )

    plt.figure()

    plt.pcolormesh(
        times,
        frequencies,
        magnitude,
        shading="gouraud"
    )

    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.title("STFT Spectrogram")

    plt.colorbar(
        label="Magnitude"
    )

    plt.show()


if __name__ == "__main__":

    print("Testing analyzer.py...")
    print()

    sample_rate = 1000
    duration = 1
    frequency = 50
    amplitude = 1

    t = np.arange(
        0,
        duration,
        1 / sample_rate
    )

    test_signal = amplitude * np.sin(
        2 * np.pi * frequency * t
    )

    print("Test signal created.")
    print(f"Frequency   : {frequency} Hz")
    print(f"Sample rate : {sample_rate} Hz")
    print(f"Samples     : {len(test_signal)}")
    print()

    frequencies, magnitude = calculate_fft(
        test_signal,
        sample_rate
    )

    print("FFT calculation successful!")
    print(
        f"Number of FFT frequency points : "
        f"{len(frequencies)}"
    )

    print()

    stft_frequencies, stft_times, stft_magnitude = (
        calculate_stft(
            test_signal,
            sample_rate
        )
    )

    print("STFT calculation successful!")
    print(
        f"Number of STFT frequency points : "
        f"{len(stft_frequencies)}"
    )

    print(
        f"Number of STFT time points : "
        f"{len(stft_times)}"
    )

    print()
    print("analyzer.py is working correctly!")