from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

#this is for the amp vs time graph
class WaveformPlotWidget(PlotWidget):
    def __init__(self):
        super().__init__()
        self.setYRange(-1,1)
        self.curve = self.plot(pen='c')

    def update_plot(self,data):
        self.curve.setData(data)
