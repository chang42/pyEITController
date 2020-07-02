from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication
from PyQt5.QtCore import QTimer

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

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.updatePlot)

    def updatePlot(self):
        self.curve = self.plot_view.plot(pen='y')
        self.curve.setData(self.data)

    def startAcquire(self):
        pass

    def stopAcquire(self):
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