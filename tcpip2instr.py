import sys
import os
import signal
import time
import logging
import gpib

sys.path.append(os.path.abspath('../python-vxi11-server/'))
import vxi11_server as Vxi11

def signal_handler(signal, frame):
    logger.info('Handling Ctrl+C!')
    instr_server.close()
    sys.exit(0)
                                        
class GPIBDevice(Vxi11.InstrumentDevice):
    READ_BLOCK_SIZE = 16384
    def __init__(self, device_name, device_lock):
        super(GPIBDevice, self).__init__(device_name, device_lock)
        self.gpib_id = int(device_name.split(",")[1])
        self.gpib_handle = gpib.dev(0, self.gpib_id)
        
    def device_write(self, opaque_data, flags, io_timeout):
        error = Vxi11.Error.NO_ERROR
        try:
            gpib.write(self.gpib_handle, opaque_data)
        except gpib.GpibError:
            error = Vxi11.Error.IO_ERROR
        return error
    
    def device_read(self, request_size, term_char, flags, io_timeout):
        error = Vxi11.Error.NO_ERROR
        reason = 4  # TODO: should be Vxi11.RX_END
        read_bytes = self.READ_BLOCK_SIZE
        result = []
        while read_bytes == self.READ_BLOCK_SIZE:
            try:
                read_block = gpib.read(self.gpib_handle, read_bytes)
            except gpib.GpibError:
                return Vxi11.Error.IO_ERROR, ""
            read_bytes = len(read_block)
            result.extend(read_block)
        return error, reason, bytearray(result)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to exit')
    logger.info('starting time_device')
    
    # create a server, attach a device, and start a thread to listen for requests
    instr_server = Vxi11.InstrumentServer()
    for i in range(1, 16):
        instr_server.add_device_handler(GPIBDevice, "gpib,%d" % i)
    instr_server.listen()

    # sleep (or do foreground work) while the Instrument threads do their job
    while True:
        time.sleep(1)

        
