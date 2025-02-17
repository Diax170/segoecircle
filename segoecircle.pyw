import tkinter as tk
from tkinter import font
from tkinter import messagebox
import sys


# Constants

FONT = 'Segoe Boot Semilight'

# Unicode range for the Windows 10 boot circle
CHARS_10 = tuple(chr(code) for code in range(0xE052, 0xE0C6 + 1))

# Unicode range for the Windows 11 boot circle
CHARS_11 = tuple(chr(code) for code in range(0xE100, 0xE176 + 1))

# Constants related to animation speed, you can change them if you want
REFRESH_DELAY_10 = 25  # Refresh delay in ms
RESET_INTERVAL_10 = 250  # Reset interval in ms, set to 0, None or False to disable

# Similar constants for the Windows 11 circle
REFRESH_DELAY_11 = 25
RESET_INTERVAL_11 = None


# Basic window config
root = tk.Tk()
root.withdraw()  # Temporarily hide the window
root.title('Windows loading circle')
root.geometry('200x200')


# Label for displaying the boot animation
label = tk.Label(root, text=CHARS_10[0], font=(FONT, 48))
label.pack(expand=True)


# Check if the font is installed, otherwise notify the user and exit
if FONT not in font.families():
    messagebox.showerror('Font not installed', f'The "{FONT}" font required to run this program is not installed.\n'
                                                'Please install it and restart the program.\n'
                                                'Click OK (or press Enter) to exit.')
    sys.exit()  # If the font is not present, the program will exit here


# Create a dialog window in which user selects the animation
dialog = tk.Toplevel()
dialog.title('Choose an animation')

tk.Label(dialog, text='Choose an animation with your mouse or keyboard', font=('Arial', 13)).pack(side=tk.TOP, padx=5, pady=5)  # Simple label

# Buttons and their commands
def btn_cmd(win: int):
    """
    Command for buttons in the animation selection dialog.
    :param win: if 10, means that the Windows 10 animation has been selected. If 11, Windows 11.
    :type win: int
    :raises ValueError: if provided value is invalid
    """
    global selected, chars, refresh_delay, reset_interval
    if win == 10:
        chars = CHARS_10
        refresh_delay = REFRESH_DELAY_10
        reset_interval = RESET_INTERVAL_10
    elif win == 11:
        chars = CHARS_11
        refresh_delay = REFRESH_DELAY_11
        reset_interval = RESET_INTERVAL_11
    else:
        raise ValueError(f'Invalid input: {win}')
    selected = True
    dialog.destroy()

btn_frame = tk.Frame(dialog)

win10_btn = tk.Button(btn_frame, text='Windows 10 (1)', font=('Arial', 13), command=lambda: btn_cmd(10))
win10_btn.pack(side=tk.LEFT, padx=(0, 5))

win11_btn = tk.Button(btn_frame, text='Windows 11 (2)', font=('Arial', 13), command=lambda: btn_cmd(11))
win11_btn.pack(side=tk.LEFT, padx=(0, 5))

tk.Button(btn_frame, text='Cancel (esc)', font=('Arial', 13), command=dialog.destroy).pack(side=tk.LEFT, padx=(0, 5))

btn_frame.pack(side=tk.BOTTOM, padx=5, pady=5)

# Keybinds
dialog.bind('1', lambda event: btn_cmd(10))  # Press "1" for Windows 10
dialog.bind('2', lambda event: btn_cmd(11))  # Press "2" for Windows 11
dialog.bind('<Escape>', lambda event: dialog.destroy())  # Press "Esc" to close without choosing

selected = False
dialog.wait_window()  # Wait for selection

# Quit if nothing's selected
if not selected:
    messagebox.showwarning('No selection', 'No animation has been selected.\nPress OK (or Enter on your keyboard) to exit.')
    sys.exit()

root.deiconify()  # Recover the main window


def update():
    """Updates the circle animation."""
    global index

    # Update the label
    label.config(text='' if index == -1 else chars[index])

    if index == -1:  # If displaying the blank character, do the reset interval
        index = 0
        root.after(reset_interval, update)
        return

    index += 1
    if index == len(chars):  # If the index is going to reset
        if reset_interval:  # If reset interval is enabled
            index = -1  # Flag to enable the blank character
        else:
            index = 0  # Normally reset the counter

    root.after(refresh_delay, update)


# Start playing the animation
index = 0
update()

root.mainloop()
