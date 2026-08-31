import pyautogui

def handle_key(key, config):
    action = config["keys"].get(key)
    
    if action is None:
        return
    
    action_type     = action.get("type")
    action_value    = action.get("value")
    
    if action_type == "text":
        pyautogui.typewrite(action_value)