import sys
import os
import signal
import time
import logging
#import tcpip2instr_gpib
import tcpip2instr_serial

sys.path.append(os.path.abspath('../python-vxi11-server/'))
import vxi11_server as Vxi11

def signal_handler(signal, frame):
    logger.info('Handling Ctrl+C!')
    instr_server.close()
    sys.exit(0)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to exit')
    logger.info('starting time_device')
    
    # create a server, attach a device, and start a thread to listen for requests
    instr_server = Vxi11.InstrumentServer()

# GPIB
#    for i in range(1, 16):
#        instr_server.add_device_handler(GPIBDevice, "gpib,%d" % i)

# Serial
    instr_server.add_device_handler(tcpip2instr_serial.SerialDevice, "serial,ACM1")

    instr_server.listen()

    # sleep (or do foreground work) while the Instrument threads do their job
    while True:
        time.sleep(1)
