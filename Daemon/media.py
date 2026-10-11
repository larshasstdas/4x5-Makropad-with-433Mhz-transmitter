import pyautogui
from pycaw.pycaw import AudioUtilities

# action value:                              
# volumeup, volumedown                      sets volume
# playpause                                 starts or stops active media (depending on current state)
# next, prev                                next song/video                            
# volumemute, micmute, bothmute             mutes and unmutes volume (depending on current state)

def handle_media(value):
    global current_mode_index, current_brightness, current_speed, current_hue, led_update

    if value == "volumeup":
        changevolume(1)
    elif value == "volumedown":
        changevolume(-1)
    elif value == "playpause":
        pyautogui.press("playpause")
    elif value == "next":
        pyautogui.press("nexttrack")
    elif value == "prev":
        pyautogui.press("prevtrack")
    elif value == "volumemute":
        volumemute()
    elif value == "micmute":
        micmute()
    elif value == "bothmute":
        bothmute()
    else:
        return
    
def changevolume(n):
    # n is the increament for volume change
    device = AudioUtilities.GetSpeakers()
    if device is None:
        return
    volume = device.volume_percent + n
    if volume > 100:
        volume = 100
    if volume < 0:
        volume = 0
    device.volume_percent = volume
    
def volumemute():
    device = AudioUtilities.GetSpeakers()
    if device is None:
        return
    volume = device.EndpointVolume
    if volume.GetMute():
        volume.SetMute(0, None)
    else:
        volume.SetMute(1, None)
        
def micmute():
    device = AudioUtilities.GetMicrophone()
    if device is None:
        #print("not found")
        return
    #print("raw:", type(device))
    if not hasattr(device, "EndpointVolume"):
        device = AudioUtilities.CreateDevice(device)
        
    #print("dev:", type(device), device.FriendlyName)
    volume = device.EndpointVolume
    if volume.GetMute():
        volume.SetMute(0, None)
    else:
        volume.SetMute(1, None)

def bothmute():
    device = AudioUtilities.GetSpeakers()
    if device is None:
        return
    devvolume = device.EndpointVolume
    
    mic = AudioUtilities.GetMicrophone()
    if mic is None:
        return
    if not hasattr(mic, "EndpointVolume"):
        mic = AudioUtilities.CreateDevice(mic)
    micvolume = mic.EndpointVolume
    
    if devvolume.GetMute() == micvolume.GetMute():
        if devvolume.GetMute():
            devvolume.SetMute(0, None)
            micvolume.SetMute(0, None)
        else:
            devvolume.SetMute(1, None)
            micvolume.SetMute(1, None)
            
    elif devvolume.GetMute():
        micvolume.SetMute(1, None)
        
    elif micvolume.GetMute():
        devvolume.SetMute(1, None)
    