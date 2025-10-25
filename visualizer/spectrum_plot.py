from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

#this is for the freq domain graph
class SpectrumPlot(PlotWidget):
    def __init__(self):
        super().__init__()
        self.setLabel('bottom', 'Frequency', units='Hz')
        self.setLabel('left', 'Magnitude')
        self.setLogMode(x=False, y=True)
        self.curve = self.plot(pen='y')
        self.setAntialiasing(True)

    def update_plot(self, fft_vals, fft_freqs):
        self.curve.setData(fft_freqs, fft_vals)
