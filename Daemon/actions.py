import pyautogui
import os
import webbrowser
import led
from led import handle_led
from media import handle_media

#TYPES
#text:          a letter/number/word
#hotkey:        keycombination e.g. Copy&Paste
#media:         volumeup, volumedown, playpause, volumemute
#led:           nextMode, lastMode, brighten, darken
#overlay        default, led, volume, ...
#url:           opens url in actions_value
#launch:        opens a programm/file/folder, the path needs to be in actions_value
#inactive:      no function

def handle_key(key, config, conn):    
    
    layout = config["layouts"].get(led.current_layout)
    if layout is None:
        return
    
    action = layout.get(key)
    if action is None:
        return
    
    action_type     = action.get("type")
    action_value    = action.get("value")
    
    if action_type == "overlay":
        if action_value in config["layouts"]:
            led.current_layout = action_value
            led.led_update = True
    elif action_type == "inactive":
        pass
    elif action_type == "text":
        pyautogui.typewrite(action_value)
    elif action_type == "hotkey":
        keys = action_value.split("+")
        pyautogui.hotkey(*keys)
    elif action_type == "led":
        handle_led(action_value)
    elif action_type == "media":
        handle_media(action_value)
    #elif action_type == "url":
    #    webbrowser.open(action_value)
    #elif action_type == "launch":
    #    os.startfile(action_value)
    #elif action_type == "makro":