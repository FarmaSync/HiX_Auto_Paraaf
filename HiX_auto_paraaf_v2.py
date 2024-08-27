import tkinter as tk
from tkinter import PhotoImage
from base64 import b64decode
import keyboard
import pyautogui
import time
from threading import Thread
import pydirectinput as pyd

class ScriptRunner:
    def __init__(self):
        self.is_running = False  # Initialize is_running
        self.stop_thread = True  # Initialize stop_thread

        self.root = tk.Tk()
        self.root.title('HiX Auto Paraaf')

        img64 = r"""
                ... (image data here) ...
                """
        icon = PhotoImage(data=b64decode(img64))
        self.root.iconphoto(False, icon, icon)

        background_color = 'white'
        self.root.config(background=background_color)

        # Make the window non-minimizable
        self.root.attributes("-topmost", True)

        # Set dimensions and resizability
        self.root.geometry("300x300")  # Adjusted size for new widgets
        self.root.resizable(False, False)  # Disallow resizing in both directions

        # Add a title label above the radio buttons
        title_label = tk.Label(self.root, text="Selecteer een optie:",
                               bg=background_color,
                               font=("Helvetica", 14, 'bold'), pady=0)
        title_label.pack()

        # Radio buttons
        self.selection_var = tk.StringVar()
        self.selection_var.set("Cyto")  # Default selection

        self.cyto_radio = tk.Radiobutton(self.root, 
                                         text="Cyto (mét afleveren)", 
                                         bg=background_color,
                                         variable=self.selection_var, value="Cyto")
        self.cyto_radio.pack()

        self.cgv_radio = tk.Radiobutton(self.root, 
                                        text="CGV (zonder afleveren)", 
                                        bg=background_color,
                                        variable=self.selection_var, value="CGV")
        self.cgv_radio.pack()

        # Delay time inputs
        tk.Label(self.root, text="Key Delay (seconds):", bg=background_color).pack()
        self.key_delay_entry = tk.Entry(self.root, width=5)
        self.key_delay_entry.insert(0, "1.8")
        self.key_delay_entry.pack()

        tk.Label(self.root, text="Cyto Extra Delay (seconds):", bg=background_color).pack()
        self.cyto_delay_entry = tk.Entry(self.root, width=5)
        self.cyto_delay_entry.insert(0, "1.0")
        self.cyto_delay_entry.pack()

        # Start & Stop buttons        
        self.start_button = tk.Button(self.root, text="Start", 
                                      command=self.start_script, 
                                      bg="#8AE34A", 
                                      font=("Helvetica", 14), 
                                      fg='Black')
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Stop", 
                                     command=self.stop_script, 
                                     bg="#E3584B", font=("Helvetica", 14),
                                     fg='White', 
                                     state=tk.DISABLED)
        self.stop_button.pack()

        self.status_label = tk.Label(self.root, text="",
                                     bg=background_color,
                                     font=("Helvetica", 12))
        self.status_label.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def simulate_key_presses(self):
        def press_keys(keys):
            for key in keys:
                pyd.keyDown(key)
            for key in keys:
                pyd.keyUp(key)

        key_delay = float(self.key_delay_entry.get())
        cyto_delay = float(self.cyto_delay_entry.get())

        while self.is_running and not self.stop_thread:
            time.sleep(key_delay)
            press_keys(['ctrl', 'alt', 'p'])

            time.sleep(0.5)
            press_keys(['ctrl', 'alt', 'n'])

            if self.selection_var.get() == 'Cyto':
                time.sleep(cyto_delay)
                press_keys(['ctrl', 'alt', 't'])

            print("Series of key presses simulated with delays.")
            event2 = keyboard.read_event(suppress=False)

    def listen_for_events(self):
        while not self.stop_thread:
            event = keyboard.read_event(suppress=False)
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'esc':
                    self.stop_script()
                else:
                    self.simulate_key_presses()
            else:
                time.sleep(0.1)

    def start_script(self):
        if not self.is_running:
            self.is_running = True
            self.stop_thread = False  # Reset the stop flag

            self.status_label.config(text="Running...", fg="#8AE34A")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

            # Start a separate thread to run the script
            self.script_thread = Thread(target=self.listen_for_events)
            self.script_thread.start()

        else:
            print("Script is already running.")

    def stop_script(self):
        if self.is_running:
            self.is_running = False
            self.stop_thread = True  # Set the stop flag

            self.status_label.config(text="Stopped", fg="#E3584B")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

        else:
            print("Script is not running.")

    def on_close(self):
        self.stop_script()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    script_gui = ScriptRunner()
    script_gui.run()
