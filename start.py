from PyQt5.QtWidgets import QApplication

from osc import Oscilloscope
from views import StartWindow

import numpy as np

rigol = Oscilloscope('TCPIP::192.168.1.163::INSTR')

rigol.open()

# rigol.write(':WAVeform:FORMat ASCii')
# rigol.write(':WAVeform:SOURce CHANnel1')

# data = rigol.query(':WAVeform:DATA?')

# data_as_array = np.array(data.split(',')[:-1], dtype=np.float)

app = QApplication([])
start_window = StartWindow(rigol)
start_window.show()
app.exit(app.exec_())

rigol.close()