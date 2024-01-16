from pywinauto import Application
import time

def simulate_key_presses_partial_title(partial_title):
    app = Application().connect(title_re=partial_title, visible=True)
    target_window = app.top_window()

    # Simulate key presses with delays
    time.sleep(1.5)
    target_window.type_keys("^%p")
    time.sleep(0.5)
    target_window.type_keys("^%n")
    time.sleep(1)
    target_window.type_keys("^%t")

    print(f"Series of key presses simulated with delays in a window with partial title: '{partial_title}'.")

# Example of how to use the function with a partial title
partial_title = 'HiX'  # Replace with the actual partial title
simulate_key_presses_partial_title(partial_title)
