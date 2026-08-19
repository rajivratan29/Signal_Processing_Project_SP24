import sys

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QComboBox,
    QLineEdit,
)


app = QApplication(sys.argv)

window = QWidget()

window.setWindowTitle(
    "Signal Generator and Analyzer"
)

window.resize(800, 600)


# Signal selection

signal_label = QLabel(
    "Select Signal:",
    parent=window
)

signal_label.move(50, 50)


signal_box = QComboBox(
    parent=window
)

signal_box.addItems([
    "Sine",
    "Cosine",
    "Square",
    "Triangle",
    "Sinc",
    "Chirp",
])

signal_box.move(150, 45)
signal_box.resize(200, 30)


# Amplitude

amplitude_label = QLabel(
    "Amplitude:",
    parent=window
)

amplitude_label.move(50, 100)


amplitude_input = QLineEdit(
    parent=window
)

amplitude_input.move(150, 95)
amplitude_input.resize(200, 30)


# Duration

duration_label = QLabel(
    "Duration (s):",
    parent=window
)

duration_label.move(50, 150)


duration_input = QLineEdit(
    parent=window
)

duration_input.move(150, 145)
duration_input.resize(200, 30)


# Sampling rate

sample_rate_label = QLabel(
    "Sampling Rate:",
    parent=window
)

sample_rate_label.move(50, 200)


sample_rate_input = QLineEdit(
    parent=window
)

sample_rate_input.move(150, 195)
sample_rate_input.resize(200, 30)


window.show()

sys.exit(app.exec())

