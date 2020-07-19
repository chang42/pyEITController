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

    def getWave(self, channel=1, type='NORMal', format='ASCii'):
        self.instance.write(':WAVeform:FORMat %s' % format)
        self.instance.write(':WAVeform:SOURce CHANnel%d' % channel)
        wave_data = self.instance.query(':WAVeform:DATA?')
        wave_data_asarray = np.array(wave_data.split(',')[:-1], dtype=np.float)
        return wave_data_asarray

    def getParam(self):
        param = self.instance.query(':WAVeform:PREamble?')
        format = ['Byte', 'Word', 'Ascii'][int(param.split(',')[0])]
        type = ['Normal', 'Maximum', 'Raw'][int(param.split(',')[1])]
        points = int(param.split(',')[2])
        count = int(param.split(',')[3])
        xincrement = float(param.split(',')[4])
        xorigin = float(param.split(',')[5])
        xreference = float(param.split(',')[6])
        yincrement = float(param.split(',')[7])
        yorigin = float(param.split(',')[8])
        yreference = float(param.split(',')[9])
        return {'format':format, 'type':type, 'points':points, 'count':count, 'xincrement':xincrement, 'xorigin':xorigin, 'xreference':xreference, 'yincrement':yincrement, 'yorigin':yorigin, 'yreference':yreference}

if __name__ == '__main__':
    rigol = Oscilloscope('TCPIP::192.168.1.163::INSTR')
    rigol.open()
    print(rigol.query('*IDN?'))
    print(rigol.getParam())
    rigol.close()