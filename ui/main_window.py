from PyQt5.QtWidgets import QMainWindow



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Visualizer")
        self.resize(800, 600)
        self.show()
