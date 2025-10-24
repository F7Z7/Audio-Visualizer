from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from visualizer.waveform_plot import WaveformPlot
from visualizer.spectrum_plot import SpectrumPlot

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Visualizer")
        self.resize(500, 500)
        self.show()
        self.initUI()

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

        # button layout
        self.button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")

        self.start_button.clicked.connect(self.start_visualization)
        self.stop_button.clicked.connect(self.stop_visualization)

        for buttons in [self.start_button, self.stop_button]:
            self.button_layout.addWidget(buttons)

        for layout in [self.visualizer_layout, self.button_layout]:
            self.main_layout.addLayout(layout)

    def start_visualization(self):
        pass

    def stop_visualization(self):
        pass
