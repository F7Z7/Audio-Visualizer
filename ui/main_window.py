from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton,
                             QHBoxLayout, QComboBox, QFileDialog, QLineEdit,
                             QLabel, QGroupBox, QMessageBox)
from PyQt5.QtCore import Qt
from visualizer.waveform_plot import WaveformPlot
from visualizer.spectrum_plot import SpectrumPlot
from audio.audio_stream import AudioStream
from audio.audio_process import compute_fft
from audio.audio_file_input import AudioFileInput


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Visualizer")
        self.resize(1000, 700)

        # State variables
        self.stream_started = False
        self.audio_input_live = True
        self.file_path = None
        self.audio_stream = None
        self.audio_file_input = None

        self.initUI()
        self.show()

    def initUI(self):
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.main_layout = QVBoxLayout(self.centralwidget)
        self.main_layout.setSpacing(15)

        # Input controls section
        self.create_input_controls()

        # Visualizer section
        self.create_visualizers()

        # Control buttons section
        self.create_control_buttons()

        # Status bar
        self.statusBar().showMessage("Ready")

    def create_input_controls(self):
        """Create input method selection controls"""
        input_group = QGroupBox("Input Settings")
        input_layout = QVBoxLayout()

        # Input method selection row
        method_layout = QHBoxLayout()
        method_label = QLabel("Input Method:")
        self.select_input_method = QComboBox()
        self.select_input_method.addItems(["Live Device Input", "Audio File from Device"])
        self.select_input_method.currentIndexChanged.connect(self.on_input_method_changed)

        method_layout.addWidget(method_label)
        method_layout.addWidget(self.select_input_method, 1)

        # File selection row
        file_layout = QHBoxLayout()
        self.select_audio_file = QPushButton("Browse...")
        self.select_audio_file.clicked.connect(self.audio_input_file)
        self.select_audio_file.setEnabled(False)
        self.select_audio_file.setMaximumWidth(100)

        self.audio_file_path = QLineEdit()
        self.audio_file_path.setPlaceholderText("No file selected")
        self.audio_file_path.setReadOnly(True)

        file_layout.addWidget(QLabel("Audio File:"))
        file_layout.addWidget(self.audio_file_path, 1)
        file_layout.addWidget(self.select_audio_file)

        input_layout.addLayout(method_layout)
        input_layout.addLayout(file_layout)
        input_group.setLayout(input_layout)

        self.main_layout.addWidget(input_group)

    def create_visualizers(self):

        visualizer_group = QGroupBox("Visualization")
        self.visualizer_layout = QHBoxLayout()

        self.time_domain_graph = WaveformPlot()
        self.freq_domain_graph = SpectrumPlot()

        self.visualizer_layout.addWidget(self.time_domain_graph)
        self.visualizer_layout.addWidget(self.freq_domain_graph)

        visualizer_group.setLayout(self.visualizer_layout)
        self.main_layout.addWidget(visualizer_group, 1)

    def create_control_buttons(self):
        control_group = QGroupBox("Controls")
        self.button_layout = QHBoxLayout()

        self.start_button = QPushButton(" Start")
        self.stop_button = QPushButton(" Stop")
        self.reset_button = QPushButton(" Reset View")

        for btn in [self.start_button, self.stop_button, self.reset_button]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet("QPushButton { font-weight: bold; }")
            self.button_layout.addWidget(btn)

        self.start_button.clicked.connect(self.start_visualization)
        self.stop_button.clicked.connect(self.stop_visualization)
        self.reset_button.clicked.connect(self.reset_view)

        self.stop_button.setEnabled(False)



        self.button_layout.addStretch()


        control_group.setLayout(self.button_layout)
        self.main_layout.addWidget(control_group)

    def on_input_method_changed(self, index):

        self.audio_input_live = (index == 0)
        self.select_audio_file.setEnabled(not self.audio_input_live)
        self.audio_file_path.setEnabled(not self.audio_input_live)

        if self.audio_input_live:
            self.audio_file_path.clear()
            self.file_path = None
            self.statusBar().showMessage("Mode: Live microphone input")
        else:
            self.statusBar().showMessage("Mode: Audio file playback")

    def audio_input_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            "",
            "Audio Files (*.wav *.mp3 *.flac *.ogg *.m4a)"
        )
        if file_path:
            self.file_path = file_path
            self.audio_file_path.setText(file_path)
            self.statusBar().showMessage(f"Selected: {file_path}")

    def start_visualization(self):
        """Start or resume visualization"""
        if self.stream_started:


            self.start_button.setEnabled(False)
            self.statusBar().showMessage("▶ Resumed")
            return

        try:
            if self.audio_input_live:
                if not self.audio_stream:
                    self.audio_stream = AudioStream(callback=self.update_plots)
                self.audio_stream.start()
                self.statusBar().showMessage("🎤 Recording from microphone...")
            else:
                if not self.file_path:
                    QMessageBox.warning(self, "No File Selected",
                                        "Please select an audio file first.")
                    return
                self.audio_file_input = AudioFileInput(
                    audio_file_path=self.file_path,
                    callback=self.update_plots
                )
                self.audio_file_input.start()
                self.statusBar().showMessage(f"▶ Playing: {self.file_path}")

            self.stream_started = True
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.select_input_method.setEnabled(False)
            self.select_audio_file.setEnabled(False)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start: {str(e)}")
            self.statusBar().showMessage("Error starting visualization")



    def stop_visualization(self):

        if not self.stream_started:
            return

        try:
            if self.audio_stream:
                self.audio_stream.stop()

            if self.audio_file_input:
                self.audio_file_input.stop()
                self.audio_file_input = None

            self.stream_started = False
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.select_input_method.setEnabled(True)
            self.select_audio_file.setEnabled(not self.audio_input_live)

            self.statusBar().showMessage("Stopped")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to stop: {str(e)}")

    def update_plots(self, data):

        try:
            # Update waveform
            self.time_domain_graph.update_plot(data)

            # Get sample rate from appropriate source
            if self.audio_input_live and self.audio_stream:
                sample_rate = self.audio_stream.sample_rate
            elif self.audio_file_input:
                sample_rate = self.audio_file_input.sample_rate
            else:
                sample_rate = 44100  # Default fallback

            # Compute and update FFT
            fft_data, fft_freqs = compute_fft(data, sample_rate)
            self.freq_domain_graph.update_plot(fft_data, fft_freqs)

        except Exception as e:
            print(f"Error updating plots: {e}")

    def reset_view(self):
        """Reset zoom / axes for both plots"""
        self.time_domain_graph.reset_range()
        self.freq_domain_graph.reset_range()
        self.statusBar().showMessage("View reset")

    def closeEvent(self, event):

        self.stop_visualization()
        event.accept()