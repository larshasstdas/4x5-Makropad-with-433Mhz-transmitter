from serial_comm import sendData
import colorsys

BYTE_MODE = ord('M')
BYTE_LED  = ord('L')

MODE_STATIC    = 0
MODE_BREATHING = 1
MODE_RAINBOW   = 2

HUE_STEP_COARSE = 6000
HUE_STEP_FINE   = 500

MODES = [MODE_STATIC, MODE_RAINBOW, MODE_BREATHING]
current_mode_index = 0
current_brightness = 255
current_speed = 100
current_hue = 0

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
    global current_mode_index, current_brightness, current_speed, current_hue, led_update

    if value == "nextMode":
        current_mode_index = (current_mode_index + 1) % len(MODES)
    elif value == "lastMode":
        current_mode_index = (current_mode_index - 1) % len(MODES)
    elif value == "brighten":
        current_brightness = min(255, current_brightness + 15)
    elif value == "darken":
        current_brightness = max(0, current_brightness - 15)
    elif value == "nextColor":
        current_hue = (current_hue + HUE_STEP_COARSE) % 65536
    elif value == "lastColor":
        current_hue = (current_hue - HUE_STEP_COARSE) % 65536
    elif value == "nextColorFine":
        current_hue = (current_hue + HUE_STEP_FINE) % 65536
    elif value == "lastColorFine":
        current_hue = (current_hue - HUE_STEP_FINE) % 65536
    elif value == "faster":
        current_speed = min(255, current_speed + 20)
    elif value == "slower":
        current_speed = max(1, current_speed - 20)
    else:
        return
    
    led_update = True
        
def setMode(conn):
    mode = MODES[current_mode_index]

    if mode == MODE_STATIC:
        r, g, b = colorsys.hsv_to_rgb(current_hue / 65536, 1.0, 1.0)
        set_static(conn, int(r*255), int(g*255), int(b*255))
    elif mode == MODE_RAINBOW:
        set_rainbow(conn, current_speed)   # keine Farbe nötig
    elif mode == MODE_BREATHING:
        r, g, b = colorsys.hsv_to_rgb(current_hue / 65536, 1.0, 1.0)
        set_breathing(conn, current_speed, int(r*255), int(g*255), int(b*255))
        
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
    global led_update
    if not led_update:
        return
    getDimLayout(config, current_layout)
    setMode(conn)
    set_dim_mask(conn, [current_brightness] * 20)
    led_update = False