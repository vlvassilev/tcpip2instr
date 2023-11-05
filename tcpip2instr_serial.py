import sys
import os
import signal
import time
import logging
import serial

sys.path.append(os.path.abspath('../python-vxi11-server/'))
import vxi11_server as Vxi11

class SerialDevice(Vxi11.InstrumentDevice):
    READ_BLOCK_SIZE = 16384
    def __init__(self, device_name, device_lock):
        super(SerialDevice, self).__init__(device_name, device_lock)
        self.serial_id = device_name.split(",")[1]
        self.serial_handle = serial.Serial("/dev/tty"+self.serial_id, baudrate=115200)
        
    def device_write(self, opaque_data, flags, io_timeout):
        # TODO: handle flags/timeout
        error = Vxi11.Error.NO_ERROR
        try:
            self.serial_handle.write(opaque_data)
        except :
            error = Vxi11.Error.IO_ERROR
        return error
    
    def device_read(self, request_size, term_char, flags, io_timeout):
        # TODO handle request_size/term_char/flags/timeout
        error = Vxi11.Error.NO_ERROR
        reason = 4  # TODO: should be Vxi11.RX_END
        read_bytes = self.READ_BLOCK_SIZE
        result = []
        print("term_char=%s, io_timeout=%u"%(str(term_char), io_timeout))
        while read_bytes == self.READ_BLOCK_SIZE:
            try:
#                self.serial_handle.read_until(term_char)
                print("Reading")
#                read_block = self.serial_handle.read(size=read_bytes)
                read_block = self.serial_handle.readline()
                print("Read %d"%(len(read_block)))
                print(read_block)
            except:
                return Vxi11.Error.IO_ERROR, ""
            read_bytes = len(read_block)
            result.extend(read_block)
        return error, reason, bytearray(result)
