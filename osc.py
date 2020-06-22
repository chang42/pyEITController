import visa
import numpy as np

class Oscilloscope:
    def __init__(self, ip, *args):
        self.ip = ip
        self.address = 'TCPIP::%s::INSTR' % self.ip
        self.rm = visa.ResourceManager('@py')

    def open(self):
        self.instance = self.rm.open_resource(self.address)

    def close(self):
        if self.instance is not None:
            self.instance.close
            self.instance = None

    def write(self, cmd):
        self.instance.write('%s' % cmd)

    def read(self):
        pass

    def query(self, cmd):
        return self.instance.query('%s' % cmd)

if __name__ == '__main__':
    rigol = Oscilloscope('192.168.1.160')
    rigol.open()
    print(rigol.query('*IDN?'))
    rigol.close()