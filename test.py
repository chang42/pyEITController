from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer

import pyqtgraph as pg

from osc import Oscilloscope
from views import StartWindow

import numpy as np

rigol = Oscilloscope('USB0::0x1AB1::0x04B0::DS2D212801707::INSTR')

rigol.open()

info = rigol.query('*IDN?')
model = info.split(',')[1]

rigol.write(':WAVeform:FORMat ASCii')
rigol.write(':WAVeform:SOURce CHANnel1')

param = rigol.query(':WAVeform:PREamble?')
points = int(param.split(',')[2])

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        xincrement = float(param.split(',')[4])
        xorigin = float(param.split(',')[5])
        self.x = np.linspace(xorigin, xorigin+points*xincrement, points)
        self.y = np.zeros(points)

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)

        self.update_timer = QTimer()
        # self.update_timer.setInterval(50)
        self.update_timer.timeout.connect(self.updatePlot)
        self.update_timer.start()

    def updatePlot(self):
        param = rigol.query(':WAVeform:PREamble?')
        points = int(param.split(',')[2])
        xincrement = float(param.split(',')[4])
        xorigin = float(param.split(',')[5])
        xdata = np.linspace(xorigin, xorigin+points*xincrement, points)

        ydata = rigol.query(':WAVeform:DATA?')

        if model != 'DS2202A':
            ydata = ydata[int(ydata[1])+2:]

        ydata_as_array = np.array(ydata.split(',')[:-1], dtype=np.float)

        self.data_line.setData(xdata, ydata_as_array)

app = QApplication([])
start_window = MainWindow()
start_window.show()
app.exit(app.exec_())

rigol.close()