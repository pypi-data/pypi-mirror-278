import pyautogui
import time
import tkinter as tk

def show_click_bubble(x, y, duration=0.5):
    """
    Function to show a visual bubble at the specified screen coordinates.
    
    Args:
    x (int): The x-coordinate of the screen where the bubble will appear.
    y (int): The y-coordinate of the screen where the bubble will appear.
    duration (float): The time in seconds the bubble will be visible.
    """
    root = tk.Tk()
    root.overrideredirect(True)
    root.geometry(f"+{x}+{y}")
    root.lift()
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-alpha", 0.7)
    
    canvas = tk.Canvas(root, width=50, height=50, highlightthickness=0)
    canvas.pack()
    
    bubble = canvas.create_oval(10, 10, 40, 40, fill="blue", outline="blue")
    
    root.after(int(duration * 1000), root.destroy)
    root.mainloop()

def auto_click(interval):
    """
    Function to automatically click the mouse at a defined interval
    and show a visual bubble at the click location.
    
    Args:
    interval (float): The time interval in seconds between clicks.
    """
    while True:
        # Get the current mouse position
        x, y = pyautogui.position()
        
        # Perform the click
        pyautogui.click()
        
        # Show the visual bubble at the click location
        show_click_bubble(x, y)
        
        # Wait for the specified interval before the next click
        time.sleep(interval)

if __name__ == "__main__":
    # Define the time interval between clicks in seconds
    click_interval = 5.0  # Change this value as needed
    
    # Start the auto clicker
    auto_click(click_interval)
