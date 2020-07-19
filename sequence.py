import visa
import numpy as np

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QDoubleValidator
from dg645 import Ui_MainWindow

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

        self.lineEdit_Trig.editingFinished.connect(lambda:self.instrument.setTriggerRate(self.lineEdit_Trig.text()))
        self.lineEdit_A.editingFinished.connect(lambda:self.instrument.setDelay('A', 'T0', self.lineEdit_A.text()))
        self.lineEdit_B.editingFinished.connect(lambda:self.instrument.setDelay('B', 'T0', self.lineEdit_B.text()))
        self.lineEdit_C.editingFinished.connect(lambda:self.instrument.setDelay('C', 'T0', self.lineEdit_C.text()))
        self.lineEdit_D.editingFinished.connect(lambda:self.instrument.setDelay('D', 'T0', self.lineEdit_D.text()))
        self.lineEdit_E.editingFinished.connect(lambda:self.instrument.setDelay('E', 'T0', self.lineEdit_E.text()))
        self.lineEdit_F.editingFinished.connect(lambda:self.instrument.setDelay('F', 'T0', self.lineEdit_F.text()))
        self.lineEdit_G.editingFinished.connect(lambda:self.instrument.setDelay('G', 'T0', self.lineEdit_G.text()))
        self.lineEdit_H.editingFinished.connect(lambda:self.instrument.setDelay('H', 'T0', self.lineEdit_H.text()))


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