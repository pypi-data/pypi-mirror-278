"""
# TextPlay 💬

**Welcome to the TextPlay repository! 👋**  
This versatile Python module provides a range of text-related functions and tools to enhance your text experience in your terminal and projects.

## Features

- **Google Search 🔍:** This tool will search Google for a query and display the results. you can specify the number of results to display.

```python
from textPlay import google_search

search_query = "Python programming"
top_results = google_search(search_query, num_results=3)
print(top_results)
```
- **Morse Code Encoder/Decoder 📣:** This tool will encode and decode a message using the morse code. It will automatically detect if the input is morse code or text.

```python
from textPlay import morse

morse = Morse()

encoded_text = morse.coder("Hello, World!")
print("Encoded Text:", encoded_text)

decoded_text = morse.decoder(encoded_text)
print("Decoded Text:", decoded_text)
```

- **Box 📦:** This tool will print a box with a message and a title with specified length.

```python
from textPlay import box

title = "Title"
content = ["word 1", "word 2"]
width_percentage = 99  # Adjust as needed
box_with_title = create_box(title, content, width_percentage)
print(box_with_title)
```

- **Colors**: This tool will print text in different colors and styles.

```python
from textPlay import colors

print(f"{RED}This is red text{RESET}")
print(f"{BG_GREEN}This has a green background{RESET}")
print(f"{BOLD}This is bold text{RESET}")
```

- **Options**: This tool will display a menu with options and handle user input for navigation and selection. Main function to display a menu with options and handle user input for navigation and selection.

```python
from textPlay import options

options(option=[('Option A', lambda: print("Option A selected")),
                ('Option B', lambda: print("Option B selected")),
                ('Option C', lambda: print("Option C selected")),
                ('Option D', lambda: print("Option D selected"))],
                index=">", 
                head="Select an option:")
```

- **Password Generator**: This tool will generate a random password with the specified length.

```python
from textPlay import password_generator

password = password_generator(length=12)
print(password)
```

- **Encryption Animation**: Simulate the encryption process by displaying random special characters before revealing the actual word.

```python
from textPlay import encrypt_animation

encrypted("Hello", sleep_time=0.1, end_color=BLUE)
```

- **Progress Bar Loader**: This tool will display a progress bar with a loading animation. Simulate and display a progress bar incrementing from 0% to 100%.  

```python
from textPlay import progress_bar_loader

# Display a progress bar with custom parameters
progress_bar(length=30, symbol='*', empty_symbol='-', color_on_completion=GREEN)
```
- **CLI**: A command line interface (CLI) for textPlay.
```bash
textPlay menu
```
To display the menu. of Text Play CLI

```bash
textPlay search --search "python" --num_results 3
```

To search Google for a query with the specified number of results.

```bash
textPlay morse --input_text "Hello, World!"
```

To encode and decode morse code.
"""

# __init__.py

from .colors import *
from .Gsearch import g_search
from .morse import Morse
from .options import options
from .password_generator import create_password
from .encrypt_animation import encrypted
from .box import create_box
from .progress_bar import progress_bar_loader
from .cli import textPlay_cli

__all__ = [
    "g_search",
    "Morse",
    "options",
    "create_password",
    "encrypted",
    "create_box",
    "progress_bar_loader",
    "textPlay_cli",
]
