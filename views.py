from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication

import pyqtgraph as pg
from pyqtgraph import PlotWidget

import numpy as np

class StartWindow(QMainWindow):
    def __init__(self, data = np.zeros(100)):
        super().__init__()
        self.data = data

        self.central_widget = QWidget()

        self.plot_view = PlotWindow(self.data)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.plot_view)
        self.setCentralWidget(self.central_widget)

    def updatePlot(self):
        self.plot_view.plotData(self.data)

    def updatePlotData(self):
        pass

class PlotWindow(PlotWidget):
    def __init__(self, data = np.zeros(100)):
        super().__init__()

        self.data = data

        # set the window size
        self.resize(1080, 1080)
        # set axis
        self.showAxis('top')
        self.showAxis('right')
        
        self.plot(self.data)

        self.show()

if __name__ == '__main__':
    app = QApplication([])
    window = StartWindow()
    window.show()
    app.exit(app.exec_())