import time
import serial
import led
from config import load_config
from serial_comm import connect, readData, sendData
from actions import handle_key

TYPE_PINGPONG   = ord('P')
TYPE_KEY        = ord('K')
TYPE_MODE       = ord('M')
TYPE_LED        = ord('L')

def main():
    config = load_config()
    port = config["serial"]["port"]
    baudrate = config["serial"]["baudrate"]
    connection = connect(port, baudrate)                     
    
    while True:
        
        try:
            msg = readData(connection)
        except serial.SerialException:
            print("Verbindung verloren, versuche neu zu verbinden...")
            try:
                connection.close()
            except Exception:
                pass
            connection = connect(port, baudrate)
            continue

        if msg is not None:
            msg_type, data = msg
            if msg_type == TYPE_PINGPONG:
                sendData(connection, TYPE_PINGPONG)
            elif msg_type == TYPE_KEY and len(data) == 1:
                handle_key(f"KEY_{data[0]}", config, connection)

        led.sendLed(connection, config)
        time.sleep(0.005)
        
        
if __name__ == "__main__":
    main()           
