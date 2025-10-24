from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout


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

        self.button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")

        self.start_button.clicked.connect(self.start_visualization)
        self.stop_button.clicked.connect(self.stop_visualization)

        for buttons in [self.start_button, self.stop_button]:
            self.button_layout.addWidget(buttons)

        self.main_layout.addLayout(self.button_layout)
    def start_visualization(self):
        pass
    
    def stop_visualization(self):
        pass