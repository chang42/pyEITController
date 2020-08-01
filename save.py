from osc import Oscilloscope

import numpy as np

import time

import matplotlib.pyplot as plt

rigol = Oscilloscope('TCPIP::192.168.1.163::INSTR')

rigol.open()

acq_depth = 7000

rigol.write(':ACQuire:MDEPth %s'%acq_depth)
rigol.write(':STOP')
rigol.write(':WAVeform:SOURce CHANnel1')
rigol.write('WAVeform:MODE RAW')
rigol.write(':WAVeform:FORMat BYTE')

if acq_depth<250000:
    max_num_pts = acq_depth
else:
    max_num_pts = 250000

num_blocks = acq_depth // max_num_pts
last_block_pts = acq_depth % max_num_pts

data_as_byte = []

start_time = time.time()
for i in np.arange(num_blocks):
    if i < num_blocks:
        rigol.write(':WAVeform:STAR %s'%(i*max_num_pts+1))
        rigol.write(':WAVeform:STOP %s'%(i*max_num_pts+250000))
        rigol.write(':WAVeform:DATA?')
        data_as_byte_part = rigol.instance.read_raw()[11:max_num_pts+11]
        data_as_byte_part = np.frombuffer(data_as_byte_part, 'b')
        data_as_byte.append(data_as_byte_part)
    else:
        rigol.write(':WAVeform:STAR %s'%(num_blocks*max_num_pts+1))
        rigol.write(':WAVeform:STOP %s'%(num_blocks*max_num_pts+last_block_pts))
        data_as_byte_part = rigol.instance.read_raw()[11:max_num_pts+11]
        data_as_byte_part = np.frombuffer(data_as_byte_part, 'b')
        data_as_byte.append(data_as_byte_part)
end_time = time.time()

print(end_time-start_time)

# rigol.write(':WAVeform:STAR 250001')
# rigol.write(':WAVeform:STOP 500000')
# rigol.write(':WAVeform:DATA?')
# data_as_byte_part2 = np.frombuffer(rigol.instance.read_raw(size=250000)[11:250011], 'b')

# rigol.write(':WAVeform:STAR 500001')
# rigol.write(':WAVeform:STOP 700000')
# rigol.write(':WAVeform:DATA?')
# data_as_byte_part3 = np.frombuffer(rigol.instance.read_raw(size=200000)[11:200011], 'b')

# data_as_byte = np.concatenate((data_as_byte_part1, data_as_byte_part2, data_as_byte_part3), axis=0)
data_as_byte = np.concatenate(data_as_byte)
volts = (data_as_byte-rigol.getParam()['yorigin']-rigol.getParam()['yreference'])*rigol.getParam()['yincrement']
times = np.linspace(0, rigol.getParam()['points']*rigol.getParam()['xincrement'], volts.size)

# np.savetxt('testfile.txt', np.c_[times, volts])

# with open('testfile.txt','w') as f:
#     f.write(str(data_as_byte))

# param = rigol.query(':WAVeform:PREamble?')

plt.plot(times, volts, 'r.')

plt.show()