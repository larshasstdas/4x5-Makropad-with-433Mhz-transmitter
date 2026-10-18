from serial_comm import sendData
import colorsys
import store

BYTE_MODE = ord('M')
BYTE_LED  = ord('L')

MODE_STATIC    = 0
MODE_BREATHING = 1
MODE_RAINBOW   = 2

HUE_STEP_COARSE = 6000
HUE_STEP_FINE   = 500

MODES = [MODE_STATIC, MODE_RAINBOW, MODE_BREATHING]

current_layout = "default"
dim_layout = [255] * 20

led_update = True

def rgb_to_grb(r, g, b):
    return (g, r, b)

def set_static(conn, r, g, b):
    sendData(conn, BYTE_MODE, bytes([MODE_STATIC, *rgb_to_grb(r, g, b)]))


def set_rainbow(conn, speed):
    sendData(conn, BYTE_MODE, bytes([MODE_RAINBOW, speed]))


def set_breathing(conn, speed, r, g, b):
    sendData(conn, BYTE_MODE, bytes([MODE_BREATHING, speed, *rgb_to_grb(r, g, b)]))


def set_dim_mask(conn, factors):
    dim = bytes([(factors[i] * dim_layout[i]) >> 8 for i in range(20)])
    sendData(conn, BYTE_LED, dim)
    
def handle_led(value):
    global led_update

    if value == "nextMode":
        store.state["modeIndex"] = (store.state["modeIndex"] + 1) % len(MODES)
    elif value == "lastMode":
        store.state["modeIndex"] = (store.state["modeIndex"] - 1) % len(MODES)
    elif value == "brighten":
        store.state["brightness"] = min(255, store.state["brightness"] + 15)
    elif value == "darken":
        store.state["brightness"] = max(0, store.state["brightness"] - 15)
    elif value == "nextColor":
        store.state["hue"] = (store.state["hue"] + HUE_STEP_COARSE) % 65536
    elif value == "lastColor":
        store.state["hue"] = (store.state["hue"] - HUE_STEP_COARSE) % 65536
    elif value == "nextColorFine":
        store.state["hue"] = (store.state["hue"] + HUE_STEP_FINE) % 65536
    elif value == "lastColorFine":
        store.state["hue"] = (store.state["hue"] - HUE_STEP_FINE) % 65536
    elif value == "faster":
        store.state["modeSpeed"] = min(255, store.state["modeSpeed"] + 20)
    elif value == "slower":
        store.state["modeSpeed"] = max(1, store.state["modeSpeed"] - 20)
    else:
        return
    
    led_update = True
        
def setMode(conn):
    mode = MODES[ store.state["modeIndex"]]

    if mode == MODE_STATIC:
        r, g, b = colorsys.hsv_to_rgb(store.state["hue"] / 65536, 1.0, 1.0)
        set_static(conn, int(r*255), int(g*255), int(b*255))
    elif mode == MODE_RAINBOW:
        set_rainbow(conn, store.state["modeSpeed"])   # keine Farbe nötig
    elif mode == MODE_BREATHING:
        r, g, b = colorsys.hsv_to_rgb(store.state["hue"] / 65536, 1.0, 1.0)
        set_breathing(conn, store.state["modeSpeed"], int(r*255), int(g*255), int(b*255))
        
def getDimLayout(config, layout_name):
    layout = config["layouts"].get(layout_name, {})
    for i in range(20):
        action = layout.get(f"KEY_{i+1}")
        if action is None:
            dimValue = 0
        elif action.get("type") == "inactive":
            dimValue = action.get("value", 0)
        else:
            dimValue = 255

        if i % 10 < 5:
            j = (i // 5) * 5 + (4 - i % 5)
        else:
            j = i
        dim_layout[j] = dimValue
    
            
def sendLed(conn, config):
    getDimLayout(config, current_layout)
    setMode(conn)
    set_dim_mask(conn, [store.state["brightness"]] * 20)