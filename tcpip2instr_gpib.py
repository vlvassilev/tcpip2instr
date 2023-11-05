import sys
import os
import signal
import time
import logging
import gpib

sys.path.append(os.path.abspath('../python-vxi11-server/'))
import vxi11_server as Vxi11

class GPIBDevice(Vxi11.InstrumentDevice):
    READ_BLOCK_SIZE = 16384
    def __init__(self, device_name, device_lock):
        super(GPIBDevice, self).__init__(device_name, device_lock)
        self.gpib_id = int(device_name.split(",")[1])
        self.gpib_handle = gpib.dev(0, self.gpib_id)
        
    def device_write(self, opaque_data, flags, io_timeout):
        # TODO: handle flags/timeout
        error = Vxi11.Error.NO_ERROR
        try:
            gpib.write(self.gpib_handle, opaque_data)
        except gpib.GpibError:
            error = Vxi11.Error.IO_ERROR
        return error
    
    def device_read(self, request_size, term_char, flags, io_timeout):
        # TODO handle request_size/term_char/flags/timeout
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
