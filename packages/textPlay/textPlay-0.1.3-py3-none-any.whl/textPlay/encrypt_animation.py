import random
import time
from string import ascii_letters
from textPlay.colors import BLUE, RESET

def encrypted(word = "Encrypted 🔐", sleep_time=0.1, end_color=BLUE, special_characters="!@#$%^&*()_+-=[]{}|;:,.<>?/"):
    """
    Simulate the encryption process by displaying random special characters before revealing the actual word.

    Parameters:
    word (str): The word to be displayed.
    sleep_time (float): The time in seconds to wait before showing the next set of random characters. Default is 0.1.
    end_color (str): The ANSI escape code for the color to be applied to the final word display. Default is BLUE.
    special_characters (str): The set of special characters to randomly choose from during the simulation. Default is "!@#$%^&*()_+-=[]{}|;:,.<>?/".

    Example:
    >>> encrypted("Hello", sleep_time=0.1, end_color=BLUE)
    """
    for char in word:
        print("\r" + "".join(random.choice(special_characters) for _ in range(len(word))), end="")
        time.sleep(sleep_time)
    print(end_color + "\r" + word + RESET)

