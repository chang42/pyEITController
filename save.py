from osc import Oscilloscope

from sequence import Sequence

import numpy as np

import time

import matplotlib.pyplot as plt

rigol = Oscilloscope('TCPIP::192.168.1.160::INSTR')
rigol.open()

def getData(chan=1):
    # acq_depth = 700000

    # rigol.write(':ACQuire:MDEPth %d'%acq_depth)
    rigol.write(':STOP')
    rigol.write(':WAVeform:SOURce CHANnel%d'%chan)
    rigol.write('WAVeform:MODE RAW')
    rigol.write(':WAVeform:FORMat BYTE')

    if acq_depth<250000:
        max_num_pts = acq_depth
    else:
        max_num_pts = 250000

    num_blocks = acq_depth // max_num_pts
    last_block_pts = acq_depth % max_num_pts

    # print(num_blocks, last_block_pts)

    data_as_byte = []

    # start_time = time.time()
    for i in np.arange(num_blocks+1):
        if i < num_blocks:
            rigol.write(':WAVeform:STAR %s'%(i*max_num_pts+1))
            rigol.write(':WAVeform:STOP %s'%(i*max_num_pts+250000))
            rigol.write(':WAVeform:DATA?')
            data_as_byte_part = rigol.instance.read_raw()[11:max_num_pts+11]
            data_as_byte_part = np.frombuffer(data_as_byte_part, 'b')
            data_as_byte.append(data_as_byte_part)
            # print(i*max_num_pts+1, i*max_num_pts+250000)
        else:
            rigol.write(':WAVeform:STAR %s'%(num_blocks*max_num_pts+1))
            rigol.write(':WAVeform:STOP %s'%(num_blocks*max_num_pts+last_block_pts))
            rigol.write(':WAVeform:DATA?')
            data_as_byte_part = rigol.instance.read_raw()[11:last_block_pts+11]
            data_as_byte_part = np.frombuffer(data_as_byte_part, 'b')
            data_as_byte.append(data_as_byte_part)
            # print(num_blocks*max_num_pts+1, num_blocks*max_num_pts+last_block_pts)
            
        # data_as_byte_part = rigol.instance.read_raw()[11:max_num_pts+11]
        # data_as_byte_part = np.frombuffer(data_as_byte_part, 'b')
        # data_as_byte.append(data_as_byte_part)
    # end_time = time.time()

    # print(end_time-start_time)

    data_as_byte = np.concatenate(data_as_byte)
    # print(len(data_as_byte))
    volts = (data_as_byte-rigol.getParam()['yorigin']-rigol.getParam()['yreference'])*rigol.getParam()['yincrement']
    times = np.linspace(0, rigol.getParam()['points']*rigol.getParam()['xincrement'], volts.size)

    return times, volts

# np.savetxt('testfile.txt', np.c_[times, volts])

# with open('testfile.txt','w') as f:
#     f.write(str(data_as_byte))

# param = rigol.query(':WAVeform:PREamble?')

# times, volts = getData(2)

# plt.plot(times, volts, 'r.')

# plt.show()

rigol.write(':RUN')
acq_depth = 700000
rigol.write(':ACQuire:MDEPth %d'%acq_depth)
# time.sleep(0.5)
# rigol.write(':SINGle')
# rigol_trig_status = rigol.query(':TRIGger:STATus?')
# print(rigol_trig_status)
# query_status_counts = 0
# while rigol_trig_status != 'STOP\n':
#     rigol_trig_status = rigol.query(':TRIGger:STATus?')
#     print(rigol_trig_status)
#     query_status_counts += 1
#     print(query_status_counts)
#     time.sleep(0.1)
#     if query_status_counts > 20:
#         break

# times_chan1, volts_chan1 = getData(chan=1)
# times_chan2, volts_chan2 = getData(chan=2)

# np.savetxt('../test/testfile.txt', np.c_[times_chan1, volts_chan1, volts_chan2])

dg645 = Sequence('TCPIP::192.168.1.139::INSTR')
dg645.open()

# burst_count_list = np.array([10, 25, 50])
burst_count_list = np.array([25])
burst_period_list = 25e-3/burst_count_list
burst_param_list = np.c_[burst_count_list, burst_period_list]

for burst_count, burst_period in burst_param_list:
    for circle in np.arange(10):
        # burst_count = 50
        # burst_period = 1e-3

        dg645.write('TSRC 1')
        dg645.write('BURC %d'%burst_count)
        dg645.write('BURP %e'%burst_period)

        rigol.write(':RUN')
        time.sleep(0.5)
        rigol.write(':SINGle')
        rigol_trig_status = rigol.query(':TRIGger:STATus?')
        # print(rigol_trig_status)
        query_status_counts = 0
        while rigol_trig_status != 'STOP\n':
            rigol_trig_status = rigol.query(':TRIGger:STATus?')
            # print(rigol_trig_status)
            query_status_counts += 1
            # print(query_status_counts)
            time.sleep(0.1)
            if query_status_counts > 20:
                break

        times_chan1, volts_chan1 = getData(chan=1)
        times_chan2, volts_chan2 = getData(chan=2)

        np.savetxt('../test/pulse_probe_3.217GHz_60_+0.00A_count%d_period%e_%d.txt'%(burst_count, burst_period, circle), np.c_[times_chan1, volts_chan1, volts_chan2])
        # np.savetxt('../test/testfile.txt', np.c_[times_chan1, volts_chan1, volts_chan2])

