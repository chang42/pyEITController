import visa
import numpy as np

class Oscilloscope:
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

if __name__ == '__main__':
    rigol = Oscilloscope('192.168.1.160')
    rigol.open()
    print(rigol.query('*IDN?'))
    rigol.close()