import visa
import numpy as np

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QDoubleValidator
from uidg645 import Ui_MainWindow

import pyqtgraph as pg

class Sequence():
    def __init__(self, address, *args):
        self.address = address
        self.rm = visa.ResourceManager()

    # open resource
    def open(self):
        self.instance = self.rm.open_resource(self.address)

    # close resource
    def close(self):
        if self.instance is not None:
            self.instance.close
            self.instance = None

    # write command
    def write(self, cmd):
        self.instance.write('%s' % cmd)

    # read command
    def read(self):
        pass

    # query command
    def query(self, cmd):
        return self.instance.query('%s' % cmd)

    def setTriggerRate(self, freq):
        self.instance.write('TRAT {:s}'.format(freq))

    def setDelay(self, chann1, chann2, delay):
        channel_list = ['T0', 'T1', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        chann1_num = channel_list.index(chann1)
        chann2_num = channel_list.index(chann2)
        self.instance.write('DLAY {:d},{:d},{:s}'.format(chann1_num, chann2_num, delay))

class StartWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, instrument=None):
        super(StartWindow, self).__init__()
        self.setupUi(self)
        self.instrument = instrument

        self.DoubleValidator = QDoubleValidator()
        self.DoubleValidator.setRange(0, 1e3)
        self.DoubleValidator.setNotation(self.DoubleValidator.ScientificNotation)
        self.DoubleValidator.setDecimals(9)
        self.lineEdit_Trig.setValidator(self.DoubleValidator)
        self.lineEdit_A.setValidator(self.DoubleValidator)
        self.lineEdit_B.setValidator(self.DoubleValidator)
        self.lineEdit_C.setValidator(self.DoubleValidator)
        self.lineEdit_D.setValidator(self.DoubleValidator)
        self.lineEdit_E.setValidator(self.DoubleValidator)
        self.lineEdit_F.setValidator(self.DoubleValidator)
        self.lineEdit_G.setValidator(self.DoubleValidator)
        self.lineEdit_H.setValidator(self.DoubleValidator)

        self.lineEdit_Trig.setText('1e2')
        self.lineEdit_A.setText('0e0')
        self.lineEdit_B.setText('0e0')
        self.lineEdit_C.setText('0e0')
        self.lineEdit_D.setText('0e0')
        self.lineEdit_E.setText('0e0')
        self.lineEdit_F.setText('0e0')
        self.lineEdit_G.setText('0e0')
        self.lineEdit_H.setText('0e0')

        self.seq_curve = self.sequenceView()

        self.verticalLayout.addWidget(self.seq_curve)

        self.lineEdit_Trig.editingFinished.connect(lambda:self.instrument.setTriggerRate(self.lineEdit_Trig.text()))
        self.lineEdit_Trig.editingFinished.connect(self.updatePlot)
        self.lineEdit_A.editingFinished.connect(lambda:self.instrument.setDelay('A', 'T0', self.lineEdit_A.text()))
        self.lineEdit_A.editingFinished.connect(self.updatePlot)
        self.lineEdit_B.editingFinished.connect(lambda:self.instrument.setDelay('B', 'T0', self.lineEdit_B.text()))
        self.lineEdit_B.editingFinished.connect(self.updatePlot)
        self.lineEdit_C.editingFinished.connect(lambda:self.instrument.setDelay('C', 'T0', self.lineEdit_C.text()))
        self.lineEdit_C.editingFinished.connect(self.updatePlot)
        self.lineEdit_D.editingFinished.connect(lambda:self.instrument.setDelay('D', 'T0', self.lineEdit_D.text()))
        self.lineEdit_D.editingFinished.connect(self.updatePlot)
        self.lineEdit_E.editingFinished.connect(lambda:self.instrument.setDelay('E', 'T0', self.lineEdit_E.text()))
        self.lineEdit_E.editingFinished.connect(self.updatePlot)
        self.lineEdit_F.editingFinished.connect(lambda:self.instrument.setDelay('F', 'T0', self.lineEdit_F.text()))
        self.lineEdit_F.editingFinished.connect(self.updatePlot)
        self.lineEdit_G.editingFinished.connect(lambda:self.instrument.setDelay('G', 'T0', self.lineEdit_G.text()))
        self.lineEdit_G.editingFinished.connect(self.updatePlot)
        self.lineEdit_H.editingFinished.connect(lambda:self.instrument.setDelay('H', 'T0', self.lineEdit_H.text()))
        self.lineEdit_H.editingFinished.connect(self.updatePlot)     

    def sequenceView(self):
        trig_rate = self.lineEdit_Trig.text()
        delay_A = self.lineEdit_A.text()
        delay_B = self.lineEdit_B.text()
        delay_C = self.lineEdit_C.text()
        delay_D = self.lineEdit_D.text()
        delay_E = self.lineEdit_E.text()
        delay_F = self.lineEdit_F.text()
        delay_G = self.lineEdit_G.text()
        delay_H = self.lineEdit_H.text()

        self.curve = pg.PlotWidget()
        period = 1/float(trig_rate)
        x = np.linspace(0, period, 1000000)
        level_AB = np.zeros(1000000)
        level_AB[:int(np.floor(1000000*float(delay_A)/period))] = 3
        level_AB[int(np.floor(1000000*float(delay_A)/period)):int(np.floor(1000000*float(delay_B)/period))] = 3.9
        level_AB[int(np.floor(1000000*float(delay_B)/period)):] = 3

        level_CD = np.zeros(1000000)
        level_CD[:int(np.floor(1000000*float(delay_C)/period))] = 2
        level_CD[int(np.floor(1000000*float(delay_C)/period)):int(np.floor(1000000*float(delay_D)/period))] = 2.9
        level_CD[int(np.floor(1000000*float(delay_D)/period)):] = 2

        level_EF = np.zeros(1000000)
        level_EF[:int(np.floor(1000000*float(delay_E)/period))] = 1
        level_EF[int(np.floor(1000000*float(delay_E)/period)):int(np.floor(1000000*float(delay_F)/period))] = 1.9
        level_EF[int(np.floor(1000000*float(delay_F)/period)):] = 1

        level_GH = np.zeros(1000000)
        level_GH[:int(np.floor(1000000*float(delay_G)/period))] = 0
        level_GH[int(np.floor(1000000*float(delay_G)/period)):int(np.floor(1000000*float(delay_H)/period))] = 0.9
        level_GH[int(np.floor(1000000*float(delay_H)/period)):] = 0
        
        self.curve.setBackground('w')
        # self.curve.showAxis('right')
        self.curve.setYRange(-0.5, 4)

        self.axis = self.curve.getPlotItem().getAxis('left')
        self.axis.setTicks([[(0, 'GH'), (1, 'EF'), (2, 'CD'), (3, 'AB')]])
        # self.axis.setStyle(tickLength=0)

        self.seq_curve_AB = self.curve.plot(x, level_AB, pen=pg.mkPen(color=(255, 0, 0), width=2))
        self.seq_curve_CD = self.curve.plot(x, level_CD, pen=pg.mkPen(color=(255, 116, 0), width=2))
        self.seq_curve_EF = self.curve.plot(x, level_EF, pen=pg.mkPen(color=(0, 153, 153), width=2))
        self.seq_curve_GH = self.curve.plot(x, level_GH, pen=pg.mkPen(color=(0, 204, 0), width=2))

        return self.curve

    def updatePlot(self):
        trig_rate = self.lineEdit_Trig.text()
        delay_A = self.lineEdit_A.text()
        delay_B = self.lineEdit_B.text()
        delay_C = self.lineEdit_C.text()
        delay_D = self.lineEdit_D.text()
        delay_E = self.lineEdit_E.text()
        delay_F = self.lineEdit_F.text()
        delay_G = self.lineEdit_G.text()
        delay_H = self.lineEdit_H.text()

        period = 1/float(trig_rate)
        x = np.linspace(0, period, 1000000)
        level_AB = np.zeros(1000000)
        level_AB[:int(np.floor(1000000*float(delay_A)/period))] = 3
        level_AB[int(np.floor(1000000*float(delay_A)/period)):int(np.floor(1000000*float(delay_B)/period))] = 3.9
        level_AB[int(np.floor(1000000*float(delay_B)/period)):] = 3

        level_CD = np.zeros(1000000)
        level_CD[:int(np.floor(1000000*float(delay_C)/period))] = 2
        level_CD[int(np.floor(1000000*float(delay_C)/period)):int(np.floor(1000000*float(delay_D)/period))] = 2.9
        level_CD[int(np.floor(1000000*float(delay_D)/period)):] = 2

        level_EF = np.zeros(1000000)
        level_EF[:int(np.floor(1000000*float(delay_E)/period))] = 1
        level_EF[int(np.floor(1000000*float(delay_E)/period)):int(np.floor(1000000*float(delay_F)/period))] = 1.9
        level_EF[int(np.floor(1000000*float(delay_F)/period)):] = 1

        level_GH = np.zeros(1000000)
        level_GH[:int(np.floor(1000000*float(delay_G)/period))] = 0
        level_GH[int(np.floor(1000000*float(delay_G)/period)):int(np.floor(1000000*float(delay_H)/period))] = 0.9
        level_GH[int(np.floor(1000000*float(delay_H)/period)):] = 0

        self.seq_curve_AB.setData(x, level_AB)
        self.seq_curve_CD.setData(x, level_CD)
        self.seq_curve_EF.setData(x, level_EF)
        self.seq_curve_GH.setData(x, level_GH)
        # self.seq_curve.plot(xdata, ydata)

        # self.seq_curve.show()

if __name__ == '__main__':
    dg645 = Sequence('TCPIP::192.168.1.139::INSTR')
    dg645.open()
    print(dg645.query('*IDN?'))
    dg645.write('TSRC 0')
    app = QApplication([])
    start_window = StartWindow(dg645)
    start_window.show()
    app.exit(app.exec_())
    dg645.close()