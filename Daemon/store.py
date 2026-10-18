import json
import os

DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
STATE_PATH = os.path.join(os.path.dirname(__file__), "state.json")

config = None
state = None

def load_config():
    global config
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config =  json.load(f)
        
def load_state():
    global state
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        state =  json.load(f)
    
def write_config():
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
def write_state():
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)        
        

load_config()
load_state()