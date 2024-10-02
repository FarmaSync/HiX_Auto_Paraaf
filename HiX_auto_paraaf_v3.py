import tkinter as tk
from tkinter import PhotoImage, simpledialog, messagebox
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

        # Default delay values
        self.key_delay = 1.8
        self.pn_delay = 0.5  # Delay between ctrl+alt+p and ctrl+alt+n
        self.cyto_delay = 1.0

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
        self.root.geometry("300x350")  # Adjusted size for new widgets
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

        # Add a Settings button
        self.settings_button = tk.Button(self.root, text="Settings",
                                         command=self.open_settings,
                                         bg="#F0F0F0",
                                         font=("Helvetica", 12),
                                         fg='Black')
        self.settings_button.pack(pady=10)

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

    def open_settings(self):
        # Prompt for password
        password = simpledialog.askstring("Password", "Enter password:", show='*', parent=self.root)
        if password is None:
            return  # User cancelled
        if password != "admin123":  # Replace with desired password
            messagebox.showerror("Error", "Incorrect password.")
            return
        # Open settings window
        self.show_settings_window()

    def show_settings_window(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.grab_set()  # Make window modal
        settings_window.resizable(False, False)

        background_color = 'white'
        settings_window.config(background=background_color)

        tk.Label(settings_window, text="Adjust Time Intervals:",
                 bg=background_color,
                 font=("Helvetica", 14, 'bold'), pady=10).pack()

        # Key Delay
        tk.Label(settings_window, text="Key Delay (seconds):", bg=background_color).pack()
        key_delay_var = tk.StringVar(value=str(self.key_delay))
        key_delay_entry = tk.Entry(settings_window, textvariable=key_delay_var, width=10)
        key_delay_entry.pack(pady=5)

        # P-N Delay
        tk.Label(settings_window, text="P-N Delay (seconds):", bg=background_color).pack()
        pn_delay_var = tk.StringVar(value=str(self.pn_delay))
        pn_delay_entry = tk.Entry(settings_window, textvariable=pn_delay_var, width=10)
        pn_delay_entry.pack(pady=5)

        # Cyto Extra Delay
        tk.Label(settings_window, text="Cyto Extra Delay (seconds):", bg=background_color).pack()
        cyto_delay_var = tk.StringVar(value=str(self.cyto_delay))
        cyto_delay_entry = tk.Entry(settings_window, textvariable=cyto_delay_var, width=10)
        cyto_delay_entry.pack(pady=5)

        # Save and Cancel buttons
        button_frame = tk.Frame(settings_window, bg=background_color)
        button_frame.pack(pady=10)

        def save_settings():
            try:
                new_key_delay = float(key_delay_var.get())
                new_pn_delay = float(pn_delay_var.get())
                new_cyto_delay = float(cyto_delay_var.get())
                if new_key_delay < 0 or new_pn_delay < 0 or new_cyto_delay < 0:
                    raise ValueError
                self.key_delay = new_key_delay
                self.pn_delay = new_pn_delay
                self.cyto_delay = new_cyto_delay
                messagebox.showinfo("Success", "Settings updated successfully.")
                settings_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid positive numbers.")

        save_button = tk.Button(button_frame, text="Save", command=save_settings,
                                bg="#4CAF50", fg='White', width=10)
        save_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=settings_window.destroy,
                                  bg="#f44336", fg='White', width=10)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def simulate_key_presses(self):
        def press_keys(keys):
            for key in keys:
                pyd.keyDown(key)
            for key in keys:
                pyd.keyUp(key)

        while self.is_running and not self.stop_thread:
            time.sleep(self.key_delay)
            press_keys(['ctrl', 'alt', 'p'])

            time.sleep(self.pn_delay)  # Delay between ctrl+alt+p and ctrl+alt+n
            press_keys(['ctrl', 'alt', 'n'])

            if self.selection_var.get() == 'Cyto':
                time.sleep(self.cyto_delay)
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
            self.script_thread = Thread(target=self.listen_for_events, daemon=True)
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
