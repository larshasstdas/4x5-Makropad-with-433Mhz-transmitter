import time
import serial
import led
import pipe
import store
from serial_comm import connect, readData, sendData
from actions import handle_key

TYPE_PINGPONG   = ord('P')
TYPE_KEY        = ord('K')
TYPE_MODE       = ord('M')
TYPE_LED        = ord('L')

CONN_TIMEOUT = 5

def main():
    serial_conn = store.config["serial"]
    pipe.start_pipe()
    connection = connect(serial_conn)
    led.led_update = True
    last_conn = time.time();                     
    
    while True:
        
        try:
            msg = readData(connection)
        except serial.SerialException:
            #print("Verbindung verloren, versuche neu zu verbinden...")
            try:
                connection.close()
            except Exception:
                pass
            connection = connect(serial_conn)
            led.led_update = True
            last_conn = time.time(); 
            continue

        if msg is not None:
            last_conn = time.time(); 
            msg_type, data = msg
            if msg_type == TYPE_PINGPONG:
                sendData(connection, TYPE_PINGPONG)
            elif msg_type == TYPE_KEY and len(data) == 1:
                handle_key(f"KEY_{data[0]}", store.config, connection)


        if time.time() - last_conn > CONN_TIMEOUT:
            try:
                connection.close()
            except Exception:
                pass
            connection = connect(serial_conn)
            led.led_update = True
            last_conn = time.time(); 
            continue
        
        if led.led_update is True:
            led.led_update = False
            led.sendLed(connection, store.config)
            store.write_state()
            pipe.sendPipe({"type": "state", "state": store.state})
            
        time.sleep(0.005)
        
        
           
if __name__ == "__main__":
    main()           
