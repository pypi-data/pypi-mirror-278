"""
Terminal Menu Program

This program creates a simple terminal-based menu with options that can be navigated using the keyboard.
Users can move up and down the menu using the arrow keys and select an option by pressing Enter. The selected
option triggers an associated function.

Modules:
    - keyboard: To read keyboard events.
    - os: To clear the terminal screen.
    - time: To add a delay to the input reading loop.

Functions:
    - print_options(selected_index, option, index, head): Clears the screen and prints the menu options, highlighting the selected option.
    - options(option, index, head): Displays a menu with options and handles user input for navigation and selection.

Usage Example:
    options(option=[('Option A', lambda: print("Option A selected")), 
                    ('Option B', lambda: print("Option B selected")), 
                    ('Option C', lambda: print("Option C selected")), 
                    ('Option D', lambda: print("Option D selected"))],
                    index=">", head="Select an option:")
"""

import keyboard
import os
import time

from textPlay.colors import *

def print_options(selected_index, option, index, head):
    """
    Function to print options with highlighting for the selected option.

    Args:
        selected_index (int): The index of the currently selected option.
        option (list of tuples): A list of tuples where each tuple contains a string (option name) and a function.
        index (str): A string that represents the indicator for the selected option.
        head (str): A string that represents the heading to be displayed above the options.

    Warnings:
        - This function clears the screen before printing the options.
        - This function uses the 'cls' command on Windows and 'clear' command on Linux/MacOS.
        - This function uses the 'read_event' function from the 'keyboard' module to read keyboard events.
        - TRY NOT TO USE THIS IN YOUR PROGRAMS. SUB PROGRAMS OF `options()` CAN BE USED.
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
    if head:
        print(head)
    for i, (option_name, _) in enumerate(option):
        if i == selected_index:
            print(f"{index} {option_name}")
        else:
            print(f"  {option_name}")

def options(option: list, index=">", head=None):
    """
    Main function to display a menu with options and handle user input for navigation and selection.

    Args:
        option (list of tuples): A list of tuples where each tuple contains a string (option name) and a function.
        index (str, optional): A string that represents the indicator for the selected option. Defaults to ">".
        head (str, optional): A string that represents the heading to be displayed above the options. Defaults to None.

    Warnings:
        - This function uses the 'read_event' function from the 'keyboard' module to read keyboard events.
        - As this tracks keyboard events, it can not be used until the option is selected.

    Example:
        options(option=[('Option A', lambda: print("Option A selected")),
                        ('Option B', lambda: print("Option B selected")),
                        ('Option C', lambda: print("Option C selected")),
                        ('Option D', lambda: print("Option D selected"))],
                        index=">", 
                        head="Select an option:")

    The function displays a menu in the terminal, allowing the user to navigate the options using the 'up' and 'down' arrow keys.
    The selected option is indicated by the 'index' string. When the user presses 'Enter', the function associated with the
    selected option is executed.
    """
    selected_index = 0
    initial_print = True  # Flag to control initial printing

    try:
        while True:
            if initial_print:
                print_options(selected_index, option, index, head)
                initial_print = False
            else:
                key_pressed = keyboard.read_event(suppress=True).name

                if key_pressed == "up":
                    selected_index = (selected_index - 1) % len(option)
                    print_options(selected_index, option, index, head)
                    time.sleep(0.2)  # Add a delay to slow down the movement
                elif key_pressed == "down":
                    selected_index = (selected_index + 1) % len(option)
                    print_options(selected_index, option, index, head)
                    time.sleep(0.2)  # Add a delay to slow down the movement
                elif key_pressed == "enter":
                    option[selected_index][1]()  # Execute the function associated with the selected option
                    break
    except KeyboardInterrupt:
        loop = True
        while loop:
            print(f"{RED}KEYBOARD INTERRUPT. \nAborting...")
            loop = False
            break