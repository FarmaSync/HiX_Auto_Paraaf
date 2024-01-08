import keyboard
import pyautogui
import time

def simulate_key_presses():
    # Simulate a series of key presses with delays
    time.sleep(1.5)  #delay
    pyautogui.hotkey('ctrl', 'alt', 'p')
    
    time.sleep(0.5)  #delay
    pyautogui.hotkey('ctrl', 'alt', 'n')
    
    time.sleep(1)  # 1 second delay
    pyautogui.hotkey('ctrl', 'alt', 't')
    
    print("Series of key presses simulated with delays.")


# Keep the script running in a loop
while True:
    # Listen for key events
    event = keyboard.read_event(suppress=True)
    while event.event_type == keyboard.KEY_DOWN:
        pyautogui.hotkey(event.name)
        if event.name =='esc':
            False
        else:
            simulate_key_presses()
            # Listen for the next key event
            event = keyboard.read_event(suppress=True)


