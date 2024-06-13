from textPlay.colors import GREEN, RESET
import time

def progress_bar_report(progress, length, symbol, empty_symbol, color_on_completion):
    """
    Display a progress bar with the given parameters.

    Parameters:
    progress (float): The current progress as a float between 0 and 1.
    length (int): The total length of the progress bar.
    symbol (str): The symbol used to represent the completed portion of the progress bar.
    empty_symbol (str): The symbol used to represent the incomplete portion of the progress bar.
    color_on_completion (str): The color to use when the progress bar reaches 100%.

    Example:
    >>> progress_bar_report(0.5, 50, '█', '-', GREEN)
    |█████████████████████████-------------------------| 50.0%
    """
    filled_length = int(length * progress)
    bar = symbol * filled_length + empty_symbol * (length - filled_length)
    color = color_on_completion if progress == 1 else ''
    print(f'|{color}{bar}{RESET}| {progress:.1%}', end='\r')

def progress_bar(length=50, symbol='█', empty_symbol='-', color_on_completion=GREEN):
    """
    Simulate and display a progress bar incrementing from 0% to 100%.

    Parameters:
    length (int): The total length of the progress bar. Default is 50.
    symbol (str): The symbol used to represent the completed portion of the progress bar. Default is '█'.
    empty_symbol (str): The symbol used to represent the incomplete portion of the progress bar. Default is '-'.
    color_on_completion (str): The color to use when the progress bar reaches 100%. Default is GREEN.

    Example:
    >>> progress_bar()
    |██████████████████████████████████████████████████| 100.0%

    >>> # Display a progress bar with custom parameters
    >>> progress_bar(length=30, symbol='*', empty_symbol='-', color_on_completion=GREEN)
    |**************************************************| 100.0%
    """
    for i in range(101):
        progress = i / 100
        progress_bar_report(progress, length, symbol, empty_symbol, color_on_completion)
        time.sleep(0.01)  # Simulate some processing time

        if i == 100:
            print()

