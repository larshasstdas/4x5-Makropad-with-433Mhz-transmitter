import json
import threading
import store
import led
#from store import load_config, load_state, write_config, write_state
from multiprocessing.connection import Listener

pipeAddress = r"\\.\pipe\macropad"
AuthKey = b"Macropad"

conn = None
sendLock = threading.Lock()

def start_pipe():
    threading.Thread(target= connect_pipe, daemon=True).start()
    
    
def connect_pipe():
    global conn
    
    with Listener(pipeAddress, authkey= AuthKey) as listener:
        
        while True:
            try:
                conn = listener.accept()
                while True:
                    handlePipe(json.loads(conn.recv_bytes()))
                
            except(EOFError, OSError, ValueError, KeyError):
                conn = None 
                
def handlePipe(pipeMsg):
    
    cmd = pipeMsg.get("cmd")
    
    if cmd == "getState":
        sendPipe({"type": "state", "state": store.state})
         
    elif cmd == "getConfig":
        sendPipe({"type": "config", "config": store.config}) 
        
    elif cmd == "newConfig":
        store.config = pipeMsg["config"]
        store.write_config()
        
        if led.current_layout not in store.config["layouts"]:
            led.current_layout = "default"
            
        led.led_update = True
        
    elif cmd == "setState":
        store.state = pipeMsg["state"]
        led.led_update = True
    
def sendPipe(pipeMsg):
    global conn
    
    if conn is None:
        return
    try:
        with sendLock:
            conn.send_bytes(json.dumps(pipeMsg).encode())
            
    except OSError:
        conn = None