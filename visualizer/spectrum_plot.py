from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

#this is for the freq domain graph
class SpectrumPlot(PlotWidget):
    def __init__(self):
        super().__init__()
        self.setLogMode(x=False, y=True)
        self.curve = self.plot(pen='r')

    def update_plot(self,fft_vals):
        self.curve.setData(fft_vals)
