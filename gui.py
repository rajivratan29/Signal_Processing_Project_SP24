import sys
import sounddevice as sd

from PyQt6.QtWidgets import (QApplication,QWidget,QLabel,QComboBox,QLineEdit,QPushButton,QMessageBox)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from signal_generator import (create_time_vector,create_sinc_time_vector,generate_sine,generate_cosine,generate_square,generate_triangle,generate_sinc,generate_chirp)
from analyzer import (calculate_fft,calculate_stft)

# Create application

app = QApplication(sys.argv)

window = QWidget()

window.setWindowTitle("Signal Generator and Analyzer")

window.resize(800, 600)


# --------------------------------------------------
# Signal Selection
# --------------------------------------------------

signal_label = QLabel("Select Signal:",parent=window)

signal_label.move(50, 50)

signal_box = QComboBox(parent=window)

signal_box.addItems(["Sine","Cosine","Square","Triangle","Sinc","Chirp"])

signal_box.move(150, 45)
signal_box.resize(200, 30)


# --------------------------------------------------
# Amplitude
# --------------------------------------------------

amplitude_label = QLabel("Amplitude:",parent=window)

amplitude_label.move(50, 100)


amplitude_input = QLineEdit(parent=window)

amplitude_input.move(150, 95)
amplitude_input.resize(200, 30)


# --------------------------------------------------
# Duration
# --------------------------------------------------

duration_label = QLabel("Duration (s):",parent=window)

duration_label.move(50, 150)


duration_input = QLineEdit(parent=window)

duration_input.move(150, 145)
duration_input.resize(200, 30)


# --------------------------------------------------
# Sampling Rate
# --------------------------------------------------

sample_rate_label = QLabel("Sampling Rate:", parent=window)

sample_rate_label.move(50, 200)


sample_rate_input = QLineEdit(parent=window)

sample_rate_input.move(150, 195)
sample_rate_input.resize(200, 30)


# --------------------------------------------------
# Frequency
# --------------------------------------------------

frequency_label = QLabel("Frequency (Hz):", parent=window)

frequency_label.move(50, 250)


frequency_input = QLineEdit(parent=window)

frequency_input.move(150, 245)
frequency_input.resize(200, 30)


# --------------------------------------------------
# Phase Shift
# --------------------------------------------------

phase_label = QLabel("Phase Shift (degrees):",parent=window)

phase_label.move(50, 300)


phase_input = QLineEdit(parent=window)

phase_input.move(200, 295)
phase_input.resize(150, 30)


# --------------------------------------------------
# Duty Cycle
# --------------------------------------------------

duty_label = QLabel("Duty Cycle (%):", parent=window)

duty_label.move(50, 350)


duty_input = QLineEdit( parent=window)

duty_input.move(150, 345)
duty_input.resize(200, 30)


# --------------------------------------------------
# Initial Frequency
# --------------------------------------------------

initial_frequency_label = QLabel("Initial Frequency (Hz):",parent=window)

initial_frequency_label.move(50, 400)


initial_frequency_input = QLineEdit(parent=window)

initial_frequency_input.move(200, 395)
initial_frequency_input.resize(150, 30)


# --------------------------------------------------
# Final Frequency
# --------------------------------------------------

final_frequency_label = QLabel("Final Frequency (Hz):",parent=window)

final_frequency_label.move(50, 450)


final_frequency_input = QLineEdit(parent=window)

final_frequency_input.move(200, 445)
final_frequency_input.resize(150, 30)


# --------------------------------------------------
# Show / Hide Signal-Specific Inputs
# --------------------------------------------------

def update_inputs(signal_name):

    phase_visible = signal_name in ["Sine","Cosine"]

    duty_visible = signal_name == "Square"

    chirp_visible = signal_name == "Chirp"

    phase_label.setVisible(phase_visible)

    phase_input.setVisible(phase_visible)

    duty_label.setVisible(duty_visible)

    duty_input.setVisible(duty_visible)

    initial_frequency_label.setVisible(chirp_visible)

    initial_frequency_input.setVisible(chirp_visible)

    final_frequency_label.setVisible(chirp_visible)

    final_frequency_input.setVisible(chirp_visible)


signal_box.currentTextChanged.connect(update_inputs)

update_inputs(signal_box.currentText())

# Waveform graph

figure = Figure()

canvas = FigureCanvas(figure)

canvas.setParent(window)

canvas.move(400, 50)

canvas.resize(350, 450)

# --------------------------------------------------
# Generate Button
# --------------------------------------------------

generate_button = QPushButton("Genrate Signal",parent=window)

generate_button.move(50, 500)
generate_button.resize(300, 40)

# Play Signal Button

play_button = QPushButton("Play Signal",parent=window)

play_button.move(50, 550)
play_button.resize(140, 40)

fft_button = QPushButton("Show FFT", parent=window)

fft_button.move(200, 550)
fft_button.resize(140, 40)

generated_signal = None
generated_sample_rate = None

# --------------------------------------------------
# Generate Signal
# --------------------------------------------------

def generate_signal():
  
    try:
      global generated_signal
      global generated_sample_rate
       
      print("Generate button clicked!")

      signal_name = signal_box.currentText()

      print(
        f"Selected signal: {signal_name}"
     )

      amplitude = float(
         amplitude_input.text()
     )

      duration = float(
        duration_input.text()
     )

      sample_rate = int(
        sample_rate_input.text()
     )


      if signal_name == "Sine":

        frequency = float(
            frequency_input.text()
        )

        phase = float(
            phase_input.text()
        )

        t = create_time_vector(
            duration,
            sample_rate
        )

        x = generate_sine(
            t,
            frequency,
            amplitude,
            phase
        )


      elif signal_name == "Cosine":

        frequency = float(
            frequency_input.text()
        )

        phase = float(
            phase_input.text()
        )

        t = create_time_vector(
            duration,
            sample_rate
        )

        x = generate_cosine(
            t,
            frequency,
            amplitude,
            phase
        )


      elif signal_name == "Square":

        frequency = float(
            frequency_input.text()
        )

        duty_cycle = float(
            duty_input.text()
        )

        t = create_time_vector(
            duration,
            sample_rate
        )

        x = generate_square(
            t,
            frequency,
            amplitude,
            duty_cycle
        )


      elif signal_name == "Triangle":

        frequency = float(
            frequency_input.text()
        )

        t = create_time_vector(
            duration,
            sample_rate
        )

        x = generate_triangle(
            t,
            frequency,
            amplitude
        )


      elif signal_name == "Sinc":

        frequency = float(
            frequency_input.text()
        )

        t = create_sinc_time_vector(
            duration,
            sample_rate
        )

        x = generate_sinc(
            t,
            frequency,
            amplitude
        )


      elif signal_name == "Chirp":

        start_frequency = float(
            initial_frequency_input.text()
        )

        end_frequency = float(
            final_frequency_input.text()
        )

        t = create_time_vector(
            duration,
            sample_rate
        )

        x = generate_chirp(
            t,
            start_frequency,
            end_frequency,
            duration,
            amplitude
        )


      print(
        f"{signal_name} signal generated successfully!"
     )

      print(
        f"Number of samples: {len(x)}"
     )

      # Plot waveform
      figure.clear()




      axis = figure.add_subplot(111)




      axis.plot(
        t,
        x
     )

      axis.set_title(
        f"{signal_name} Waveform"
     )

      axis.set_xlabel(
        "Time (s)"
     )

      axis.set_ylabel(
        "Amplitude"
     )

      axis.grid(True)

      figure.tight_layout()




      canvas.draw()

      generated_signal = x
      generated_sample_rate = sample_rate
    except ValueError:

     QMessageBox.warning(window,"Invalid Input","Please enter valid numerical values.")

     # --------------------------------------------------
# Show FFT
# --------------------------------------------------

def show_fft():

    if generated_signal is None:

        QMessageBox.warning(
            window,
            "No Signal",
            "Please generate a signal first."
        )

        return

    frequencies, magnitude = calculate_fft(
        generated_signal,
        generated_sample_rate
    )

    figure.clear()

    axis = figure.add_subplot(111)

    axis.plot(
        frequencies,
        magnitude
    )

    axis.set_title(
        "FFT Spectrum"
    )

    axis.set_xlabel(
        "Frequency (Hz)"
    )

    axis.set_ylabel(
        "Magnitude"
    )

    axis.grid(True)

    figure.tight_layout()

    canvas.draw()
    
def play_signal():

    if generated_signal is None:

        QMessageBox.warning(
            window,
            "No Signal",
            "Please generate a signal first."
        )

        return

    sd.play(
        generated_signal,
        generated_sample_rate
    )
generate_button.clicked.connect(generate_signal)

play_button.clicked.connect(play_signal)

fft_button.clicked.connect(show_fft)
# --------------------------------------------------
# Start GUI
# --------------------------------------------------

window.show()

sys.exit(
    app.exec()
)