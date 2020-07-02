from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer

import pyqtgraph as pg

from osc import Oscilloscope
from views import StartWindow

import numpy as np

rigol = Oscilloscope('192.168.1.148')

rigol.open()

rigol.write(':WAVeform:FORMat ASCii')
rigol.write(':WAVeform:SOURce CHANnel1')

param = rigol.query(':WAVeform:PREamble?')

points = int(param.split(',')[2])

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.y = np.zeros(points)

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.y, pen=pen)

        self.update_timer = QTimer()
        # self.update_timer.setInterval(50)
        self.update_timer.timeout.connect(self.updatePlot)
        self.update_timer.start()

    def updatePlot(self):
        data = rigol.query(':WAVeform:DATA?')

        data = data[int(data[1])+2:]

        data_as_array = np.array(data.split(',')[:-1], dtype=np.float)

        self.data_line.setData(data_as_array)

app = QApplication([])
start_window = MainWindow()
start_window.show()
app.exit(app.exec_())

rigol.close()