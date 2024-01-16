import keyboard
import pyautogui
import time
import pydirectinput as pyd

def press_keys(keys):
    for key in keys:
        pyd.keyDown(key)
    for key in keys:
        pyd.keyUp(key)



def simulate_key_presses():
    # Simulate a series of key presses with delays
    time.sleep(1.5)  #delay
    #pyautogui.hotkey('ctrl', 'alt', 'p')
    press_keys(['ctrl', 'alt', 'p'])
    time.sleep(0.5)  #delay
    #pyautogui.hotkey('ctrl', 'alt', 'n')
    press_keys(['ctrl', 'alt', 'n'])

    time.sleep(1)  # 1 second delay
    #pyautogui.hotkey('ctrl', 'alt', 't')
    press_keys(['ctrl', 'alt', 't'])

    
    print("Series of key presses simulated with delays.")
    #pyautogui.confirm('This displays text and has an OK and Cancel button.')


# Keep the script running in a loop
while True:
    # Listen for key events
    event = keyboard.read_event(suppress=False)
    while event.event_type == keyboard.KEY_DOWN:
        pyautogui.hotkey(event.name)
        if event.name =='esc':
            break
        else:
            simulate_key_presses()
            # Listen for the next key event
            event = keyboard.read_event(suppress=False)


