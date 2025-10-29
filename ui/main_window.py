from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QComboBox
from visualizer.waveform_plot import WaveformPlot
from visualizer.spectrum_plot import SpectrumPlot
from audio.audio_stream import AudioStream
from audio.audio_process import compute_fft

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Visualizer")
        self.resize(800, 800)
        self.initUI()
        self.show()
        self.stream_started=False
        self.audio_stream = AudioStream(callback=self.update_plots)
        self.audio_input=False


    def initUI(self):
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.main_layout = QVBoxLayout(self.centralwidget)

            #visualizer layout
        self.visualizer_layout = QHBoxLayout()
        self.time_domain_graph=WaveformPlot()
        self.freq_domain_graph=SpectrumPlot()

        for plots in [self.time_domain_graph, self.freq_domain_graph]:
            self.visualizer_layout.addWidget(plots)

#combo box for selection of input method
        self.select_input_method=QComboBox()
        self.select_input_method.addItems(["Live Input","Upload From Device"])
        self.select_input_method.currentIndexChanged.connect(self.on_input_method_changed)

            # button layout
        self.button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")

        self.start_button.clicked.connect(self.start_visualization)
        self.stop_button.clicked.connect(self.stop_visualization)

        for buttons in [self.select_input_method,self.start_button, self.stop_button]:
            self.button_layout.addWidget(buttons)

        for layout in [self.visualizer_layout, self.button_layout]:
            self.main_layout.addLayout(layout)

    def on_input_method_changed(self, index):
        self.audio_input = (index == 0)


    def start_visualization(self):
        if not self.stream_started and self.audio_input:
            self.audio_stream.start()
            self.stream_started=True
    def stop_visualization(self):
        self.audio_stream.stop()
        self.stream_started=False



    def update_plots(self,data):
        self.time_domain_graph.update_plot(data)

        fft_data, fft_freqs = compute_fft(data, self.audio_stream.sample_rate)

        self.freq_domain_graph.update_plot(fft_data,fft_freqs)

