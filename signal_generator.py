import numpy as np
from scipy import signal


def create_time_vector(duration, sample_rate):
    return np.arange(0, duration, 1 / sample_rate)


def create_sinc_time_vector(duration, sample_rate):
    return np.arange(
        -duration / 2,
        duration / 2,
        1 / sample_rate
    )


def generate_sine(t, frequency, amplitude, phase=0):
    phase = np.deg2rad(phase)

    return amplitude * np.sin(
        2 * np.pi * frequency * t + phase
    )


def generate_cosine(t, frequency, amplitude, phase=0):
    phase = np.deg2rad(phase)

    return amplitude * np.cos(
        2 * np.pi * frequency * t + phase
    )


def generate_square(t, frequency, amplitude, duty_cycle=50):
    return amplitude * signal.square(
        2 * np.pi * frequency * t,
        duty=duty_cycle / 100
    )


def generate_triangle(t, frequency, amplitude):
    return amplitude * signal.sawtooth(
        2 * np.pi * frequency * t,
        width=0.5
    )


def generate_sinc(t, frequency, amplitude):
    return amplitude * np.sinc(
        frequency * t
    )


def generate_chirp(
    t,
    start_frequency,
    end_frequency,
    duration,
    amplitude,
    method="linear"
):
    return amplitude * signal.chirp(
        t,
        f0=start_frequency,
        t1=duration,
        f1=end_frequency,
        method=method
    )


if __name__ == "__main__":

    print("Testing signal_generator.py...")
    print()

    duration = 1
    sample_rate = 1000
    frequency = 5
    amplitude = 1

    t = create_time_vector(
        duration,
        sample_rate
    )

    sine = generate_sine(
        t,
        frequency,
        amplitude
    )

    cosine = generate_cosine(
        t,
        frequency,
        amplitude
    )

    square = generate_square(
        t,
        frequency,
        amplitude
    )

    triangle = generate_triangle(
        t,
        frequency,
        amplitude
    )

    sinc = generate_sinc(
        t,
        frequency,
        amplitude
    )

    chirp = generate_chirp(
        t,
        5,
        50,
        duration,
        amplitude
    )

    print("Signal generation successful!")
    print()

    print(f"Number of samples : {len(t)}")
    print(f"Duration          : {duration} seconds")
    print(f"Sample rate       : {sample_rate} Hz")
    print(f"Frequency         : {frequency} Hz")
    print(f"Amplitude         : {amplitude}")
    print()

    print("Generated signals:")
    print(f"Sine     : {len(sine)} samples")
    print(f"Cosine   : {len(cosine)} samples")
    print(f"Square   : {len(square)} samples")
    print(f"Triangle : {len(triangle)} samples")
    print(f"Sinc     : {len(sinc)} samples")
    print(f"Chirp    : {len(chirp)} samples")

    print()
    print("signal_generator.py is working correctly!")