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

    def getTriggerRate(self):
        trig_rate = self.instance.query('TRAT?')
        return float(trig_rate)

    def setDelay(self, chann1, chann2, delay):
        '''
        '''
        channel_list = ['T0', 'T1', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        chann1_num = channel_list.index(chann1)
        chann2_num = channel_list.index(chann2)
        self.instance.write('DLAY {:d},{:d},{:s}'.format(chann1_num, chann2_num, delay))

    def getDelay(self, chann):
        '''
        Set channel delay to other channels can only use T0, A-H
        '''
        channel_list = ['T0', 'T1', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        chann_num = channel_list.index(chann)
        ref_chann_num, delay = self.instance.query('DLAY?{:d}'.format(chann_num)).split(',')
        # ref_chann = channel_list[ref_chann_num]
        return [int(ref_chann_num), float(delay)]

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

        self.lineEdit_Trig.setText('%e'%self.instrument.getTriggerRate())
        self.lineEdit_A.setText('%e'%self.instrument.getDelay('A')[1])
        self.lineEdit_B.setText('%e'%self.instrument.getDelay('B')[1])
        self.lineEdit_C.setText('%e'%self.instrument.getDelay('C')[1])
        self.lineEdit_D.setText('%e'%self.instrument.getDelay('D')[1])
        self.lineEdit_E.setText('%e'%self.instrument.getDelay('E')[1])
        self.lineEdit_F.setText('%e'%self.instrument.getDelay('F')[1])
        self.lineEdit_G.setText('%e'%self.instrument.getDelay('G')[1])
        self.lineEdit_H.setText('%e'%self.instrument.getDelay('H')[1])

        self.comboBox_A.setCurrentIndex(0 if self.instrument.getDelay('A')[0]==0 else self.instrument.getDelay('A')[0]-1)
        self.comboBox_B.setCurrentIndex(0 if self.instrument.getDelay('B')[0]==0 else self.instrument.getDelay('B')[0]-1)
        self.comboBox_C.setCurrentIndex(0 if self.instrument.getDelay('C')[0]==0 else self.instrument.getDelay('C')[0]-1)
        self.comboBox_D.setCurrentIndex(0 if self.instrument.getDelay('D')[0]==0 else self.instrument.getDelay('D')[0]-1)
        self.comboBox_E.setCurrentIndex(0 if self.instrument.getDelay('E')[0]==0 else self.instrument.getDelay('E')[0]-1)
        self.comboBox_F.setCurrentIndex(0 if self.instrument.getDelay('F')[0]==0 else self.instrument.getDelay('F')[0]-1)
        self.comboBox_G.setCurrentIndex(0 if self.instrument.getDelay('G')[0]==0 else self.instrument.getDelay('G')[0]-1)
        self.comboBox_H.setCurrentIndex(0 if self.instrument.getDelay('H')[0]==0 else self.instrument.getDelay('H')[0]-1)

        self.seq_curve = self.sequenceView()

        self.verticalLayout.addWidget(self.seq_curve)

        self.lineEdit_Trig.editingFinished.connect(lambda:self.instrument.setTriggerRate(self.lineEdit_Trig.text()))
        self.lineEdit_Trig.editingFinished.connect(self.updatePlot)
        self.lineEdit_A.editingFinished.connect(lambda:self.instrument.setDelay('A', '%s'%self.comboBox_A.currentText(), self.lineEdit_A.text()))
        self.lineEdit_A.editingFinished.connect(self.updatePlot)
        self.lineEdit_B.editingFinished.connect(lambda:self.instrument.setDelay('B', '%s'%self.comboBox_B.currentText(), self.lineEdit_B.text()))
        self.lineEdit_B.editingFinished.connect(self.updatePlot)
        self.lineEdit_C.editingFinished.connect(lambda:self.instrument.setDelay('C', '%s'%self.comboBox_C.currentText(), self.lineEdit_C.text()))
        self.lineEdit_C.editingFinished.connect(self.updatePlot)
        self.lineEdit_D.editingFinished.connect(lambda:self.instrument.setDelay('D', '%s'%self.comboBox_D.currentText(), self.lineEdit_D.text()))
        self.lineEdit_D.editingFinished.connect(self.updatePlot)
        self.lineEdit_E.editingFinished.connect(lambda:self.instrument.setDelay('E', '%s'%self.comboBox_E.currentText(), self.lineEdit_E.text()))
        self.lineEdit_E.editingFinished.connect(self.updatePlot)
        self.lineEdit_F.editingFinished.connect(lambda:self.instrument.setDelay('F', '%s'%self.comboBox_F.currentText(), self.lineEdit_F.text()))
        self.lineEdit_F.editingFinished.connect(self.updatePlot)
        self.lineEdit_G.editingFinished.connect(lambda:self.instrument.setDelay('G', '%s'%self.comboBox_G.currentText(), self.lineEdit_G.text()))
        self.lineEdit_G.editingFinished.connect(self.updatePlot)
        self.lineEdit_H.editingFinished.connect(lambda:self.instrument.setDelay('H', '%s'%self.comboBox_H.currentText(), self.lineEdit_H.text()))
        self.lineEdit_H.editingFinished.connect(self.updatePlot)   

        self.comboBox_A.currentIndexChanged[str].connect(lambda:self.instrument.setDelay('A', '%s'%self.comboBox_A.currentText(), self.lineEdit_A.text()))
        self.comboBox_A.currentIndexChanged[str].connect(self.updatePlot)
        self.comboBox_B.currentIndexChanged[str].connect(lambda:self.instrument.setDelay('B', '%s'%self.comboBox_B.currentText(), self.lineEdit_B.text()))
        self.comboBox_B.currentIndexChanged[str].connect(self.updatePlot)
        self.comboBox_C.currentIndexChanged[str].connect(lambda:self.instrument.setDelay('C', '%s'%self.comboBox_C.currentText(), self.lineEdit_C.text()))
        self.comboBox_C.currentIndexChanged[str].connect(self.updatePlot)
        self.comboBox_D.currentIndexChanged[str].connect(lambda:self.instrument.setDelay('D', '%s'%self.comboBox_D.currentText(), self.lineEdit_D.text()))
        self.comboBox_D.currentIndexChanged[str].connect(self.updatePlot)
        self.comboBox_E.currentIndexChanged[str].connect(lambda:self.instrument.setDelay('E', '%s'%self.comboBox_E.currentText(), self.lineEdit_E.text()))
        self.comboBox_E.currentIndexChanged[str].connect(self.updatePlot)
        self.comboBox_F.currentIndexChanged[str].connect(lambda:self.instrument.setDelay('F', '%s'%self.comboBox_F.currentText(), self.lineEdit_F.text()))
        self.comboBox_F.currentIndexChanged[str].connect(self.updatePlot)
        self.comboBox_G.currentIndexChanged[str].connect(lambda:self.instrument.setDelay('G', '%s'%self.comboBox_G.currentText(), self.lineEdit_G.text()))
        self.comboBox_G.currentIndexChanged[str].connect(self.updatePlot)
        self.comboBox_H.currentIndexChanged[str].connect(lambda:self.instrument.setDelay('H', '%s'%self.comboBox_H.currentText(), self.lineEdit_H.text()))
        self.comboBox_H.currentIndexChanged[str].connect(self.updatePlot)

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
        delay = {'T0':0, 'A':delay_A, 'B':delay_B, 'C':delay_C, 'D':delay_D, 'E':delay_E, 'F':delay_F, 'G':delay_G, 'H':delay_H}
        reference_A = delay['%s'%self.comboBox_A.currentText()]
        reference_B = delay['%s'%self.comboBox_B.currentText()]
        reference_C = delay['%s'%self.comboBox_C.currentText()]
        reference_D = delay['%s'%self.comboBox_D.currentText()]
        reference_E = delay['%s'%self.comboBox_E.currentText()]
        reference_F = delay['%s'%self.comboBox_F.currentText()]
        reference_G = delay['%s'%self.comboBox_G.currentText()]
        reference_H = delay['%s'%self.comboBox_H.currentText()]
        delay_A = float(reference_A)+float(delay_A)
        delay_B = float(reference_B)+float(delay_B)
        delay_C = float(reference_C)+float(delay_C)
        delay_D = float(reference_D)+float(delay_D)
        delay_E = float(reference_E)+float(delay_E)
        delay_F = float(reference_F)+float(delay_F)
        delay_G = float(reference_G)+float(delay_G)
        delay_H = float(reference_H)+float(delay_H)

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
        delay = {'T0':0, 'A':delay_A, 'B':delay_B, 'C':delay_C, 'D':delay_D, 'E':delay_E, 'F':delay_F, 'G':delay_G, 'H':delay_H}
        reference_A = delay['%s'%self.comboBox_A.currentText()]
        reference_B = delay['%s'%self.comboBox_B.currentText()]
        reference_C = delay['%s'%self.comboBox_C.currentText()]
        reference_D = delay['%s'%self.comboBox_D.currentText()]
        reference_E = delay['%s'%self.comboBox_E.currentText()]
        reference_F = delay['%s'%self.comboBox_F.currentText()]
        reference_G = delay['%s'%self.comboBox_G.currentText()]
        reference_H = delay['%s'%self.comboBox_H.currentText()]
        delay_A = float(reference_A)+float(delay_A)
        delay_B = float(reference_B)+float(delay_B)
        delay_C = float(reference_C)+float(delay_C)
        delay_D = float(reference_D)+float(delay_D)
        delay_E = float(reference_E)+float(delay_E)
        delay_F = float(reference_F)+float(delay_F)
        delay_G = float(reference_G)+float(delay_G)
        delay_H = float(reference_H)+float(delay_H)

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
    # print(dg645.query('TRAT?'))
    dg645.write('TSRC 0')
    app = QApplication([])
    start_window = StartWindow(dg645)
    start_window.show()
    app.exit(app.exec_())
    dg645.close()