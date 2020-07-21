from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication, QPushButton
from PyQt5.QtCore import QTimer, QThread

import pyqtgraph as pg
from pyqtgraph import PlotWidget

import numpy as np

class StartWindow(QMainWindow):
    def __init__(self, oscilloscope = None):
        super().__init__()
        self.oscilloscope = oscilloscope

        self.central_widget = QWidget()
        # Adding click buttons for acquire frame & movie
        self.button_single_frame = QPushButton('Single Frame', self.central_widget)
        self.button_start_continous = QPushButton('Start Updating', self.central_widget)
        self.button_stop_continous = QPushButton('Stop Updating', self.central_widget)

        self.plot_view = PlotWindow()

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.button_single_frame)
        self.layout.addWidget(self.button_start_continous)
        self.layout.addWidget(self.button_stop_continous)
        self.layout.addWidget(self.plot_view)
        self.setCentralWidget(self.central_widget)

        self.button_single_frame.clicked.connect(self.updatePlot)
        self.button_start_continous.clicked.connect(self.startAcquire)
        self.button_stop_continous.clicked.connect(self.stopAcquire)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.updatePlot)

    def updatePlot(self):
        points = self.oscilloscope.getParam()['points']
        xorigin = self.oscilloscope.getParam()['xorigin']
        xincrement = self.oscilloscope.getParam()['xincrement']
        xdata = np.linspace(xorigin, xorigin+points*xincrement, points)
        ydata = self.oscilloscope.getWave()
        self.plot_view.curve.setData(xdata, ydata)

    def startAcquire(self):
        self.update_timer.start()

    def stopAcquire(self):
        self.update_timer.stop()


class PlotWindow(PlotWidget):
    def __init__(self):
        super().__init__()

        self.x = np.linspace(0, 1, 1400)
        self.y = np.zeros(1400)

        self.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.curve =  self.plot(self.x, self.y, pen=pen)

        self.show()

if __name__ == '__main__':
    app = QApplication([])
    window = StartWindow()
    window.show()
    app.exit(app.exec_())