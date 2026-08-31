import serial
import time



def connect(port, baudrate):

    while True:
        try:
            SerialObj = serial.Serial(port,baudrate, timeout=1)     
            return SerialObj
            
        except serial.SerialException:
            time.sleep(0.2)
        

def read_line(connection):

    try:
        line = connection.readline().decode("utf-8", errors="ignore").strip()
        return line if line else None
    except (serial.SerialException, OSError):
        raise ConnectionError("Serial device disconnected")

def write_line(connection, text):
    
    try:
        connection.write((text + "\n").encode("utf-8"))
    except serial.SerialException:
        pass