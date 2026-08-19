import sys
import matplotlib.pyplot as plt
from analyzer import ( plot_fft, plot_stft, )
from signal_generator import (
    create_time_vector,
    create_sinc_time_vector,
    generate_sine,
    generate_cosine,
    generate_square,
    generate_triangle,
    generate_sinc,
    generate_chirp,
)

from audio import (
    save_audio,
    play_audio,
    stop_audio,
)

from utils import (
    get_float_input,
    get_int_input,
    get_choice,
    validate_filename,
)


def choose_signal():
    print()
    print("Choose a signal:")
    print("1. Sine")
    print("2. Cosine")
    print("3. Square")
    print("4. Triangle")
    print("5. Sinc")
    print("6. Chirp")
    print()

    return get_choice(
        "Enter your choice: ",
        ["1", "2", "3", "4", "5", "6"]
    )


def generate_selected_signal(choice):
    amplitude = get_float_input(
        "Enter amplitude: ",
        minimum=0
    )

    duration = get_float_input(
        "Enter duration (seconds): ",
        minimum=0.001
    )

    sample_rate = get_int_input(
        "Enter sampling rate (Hz): ",
        minimum=1
    )

    if choice == "5":
        t = create_sinc_time_vector(
            duration,
            sample_rate
        )
    else:
        t = create_time_vector(
            duration,
            sample_rate
        )

    if choice == "1":
        frequency = get_float_input(
            "Enter frequency (Hz): ",
            minimum=0
        )

        phase = get_float_input(
            "Enter phase shift (degrees): "
        )

        x = generate_sine(
            t,
            frequency,
            amplitude,
            phase
        )

        title = (
            f"Sine Wave | "
            f"f={frequency} Hz | "
            f"A={amplitude} | "
            f"Phase={phase}°"
        )

    elif choice == "2":
        frequency = get_float_input(
            "Enter frequency (Hz): ",
            minimum=0
        )

        phase = get_float_input(
            "Enter phase shift (degrees): "
        )

        x = generate_cosine(
            t,
            frequency,
            amplitude,
            phase
        )

        title = (
            f"Cosine Wave | "
            f"f={frequency} Hz | "
            f"A={amplitude} | "
            f"Phase={phase}°"
        )

    elif choice == "3":
        frequency = get_float_input(
            "Enter frequency (Hz): ",
            minimum=0
        )

        duty_cycle = get_float_input(
            "Enter duty cycle (%): ",
            minimum=0,
            maximum=100
        )

        x = generate_square(
            t,
            frequency,
            amplitude,
            duty_cycle
        )

        title = (
            f"Square Wave | "
            f"f={frequency} Hz | "
            f"A={amplitude} | "
            f"Duty={duty_cycle}%"
        )

    elif choice == "4":
        frequency = get_float_input(
            "Enter frequency (Hz): ",
            minimum=0
        )

        x = generate_triangle(
            t,
            frequency,
            amplitude
        )

        title = (
            f"Triangle Wave | "
            f"f={frequency} Hz | "
            f"A={amplitude}"
        )

    elif choice == "5":
        frequency = get_float_input(
            "Enter frequency scaling factor: ",
            minimum=0
        )

        x = generate_sinc(
            t,
            frequency,
            amplitude
        )

        title = (
            f"Sinc Signal | "
            f"f={frequency} | "
            f"A={amplitude}"
        )

    else:
        start_frequency = get_float_input(
            "Enter initial frequency (Hz): ",
            minimum=0
        )

        end_frequency = get_float_input(
            "Enter final frequency (Hz): ",
            minimum=0
        )

        x = generate_chirp(
            t,
            start_frequency,
            end_frequency,
            duration,
            amplitude
        )

        title = (
            f"Chirp Signal | "
            f"f0={start_frequency} Hz | "
            f"f1={end_frequency} Hz | "
            f"T={duration}s | "
            f"A={amplitude}"
        )

    return t, x, sample_rate, title


def plot_signal(t, signal_data, title):
    plt.figure()

    plt.plot(
        t,
        signal_data
    )

    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)

    plt.show()


def main():
    print("=" * 50)
    print("Signal Generator and Analyzer")
    print("=" * 50)

    choice = choose_signal()

    t, signal_data, sample_rate, title = (
        generate_selected_signal(choice)
    )

    print()
    print("Signal generated successfully!")
    print(f"Number of samples : {len(signal_data)}")
    print(f"Sampling rate     : {sample_rate} Hz")
    print()

    plot_signal(
        t,
        signal_data,
        title
    )
    print()
    print("Analyzer Options:")
    print("1. FFT")
    print("2. STFT")
    print("3. Skip analyzer")

    analysis_choice = get_choice(
        "Enter your choice: ",
        ["1", "2", "3"]
    )

    if analysis_choice == "1":
        plot_fft(
            signal_data,
            sample_rate
        )

    elif analysis_choice == "2":
        plot_stft(
            signal_data,
            sample_rate
        )

    save = input(
        "Do you want to save the signal? (y/n): "
    ).strip().lower()

    if save == "y":
        filename = input(
            "Enter filename: "
        )

        filename = validate_filename(
            filename
        )

        if filename is not None:
            save_audio(
                filename,
                signal_data,
                sample_rate
            )

    play = input(
        "Do you want to play the signal? (y/n): "
    ).strip().lower()

    if play == "y":
        play_audio(
            signal_data,
            sample_rate
        )

        input(
            "Press Enter to stop playback..."
        )

        stop_audio()

    print()
    print("Program finished.")


if __name__ == "__main__":
    main()