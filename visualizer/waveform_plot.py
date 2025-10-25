from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

#this is for the amp vs time graph
class WaveformPlot(PlotWidget):
    def __init__(self):
        super().__init__()
        self.setLabel('bottom', 'Time', units='samples')
        self.setLabel('left', 'Amplitude')
        self.curve = self.plot(pen='c')
        self.setAntialiasing(True)

    def update_plot(self,data):
        self.curve.setData(data)
