from config import load_config
from serial_comm import connect, read_line, write_line
from actions import handle_key

def main():
    config = load_config()
    port = config["serial"]["port"]
    baudrate = config["serial"]["baudrate"]
    
    #print(f"Connecting with {port}...")
    connection = connect(port, baudrate)
    #print("Connected!")                       
    
    while True:

        try:
            line = read_line(connection)
        except ConnectionError:
            connection.close()
            connection = connect(port, baudrate)
            continue

        if line is None:
            continue
        

        # WakeUp Button
        if line == "PING":
            write_line(connection, "PONG")
            continue

        if line.startswith("KEY_"):
            handle_key(line, config)
        
        
if __name__ == "__main__":
    main()           
