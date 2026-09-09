import serial
import time

STARTBYTE = 0xAB

_header_read = False
_type = 0
_length = 0
_current_length = 0
_data = bytearray(60)

def connect(port, baudrate):

    while True:
        try:    
            return serial.Serial(port,baudrate, timeout=0.1) 
            
        except serial.SerialException:
            time.sleep(0.2)  

def readData(conn):
    
    global _header_read, _type, _length, _current_length, _data

    try:
        if not _header_read:
            if conn.in_waiting < 3:
                return None

            b = conn.read(1)
            if b[0] != STARTBYTE:
                return None
            _type = conn.read(1)[0]
            _length = conn.read(1)[0]
            _current_length = 0
            _header_read = True

            if _length > 60:
                _header_read = False
                return None

        while _current_length < _length and conn.in_waiting > 0:
            _data[_current_length] = conn.read(1)[0]
            _current_length += 1

        if _current_length >= _length:
            result = (_type, bytes(_data[:_length]))
            _header_read = False
            return result

        return None
    
    except serial.SerialException:
        _header_read = False
        raise

def sendData(conn, msg_type, data=b""):
    
    try:
        frame = bytes([STARTBYTE, msg_type, len(data)]) + data
        conn.write(frame)
    except serial.SerialException:
        pass