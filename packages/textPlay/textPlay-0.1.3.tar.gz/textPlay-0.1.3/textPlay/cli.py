import click
import webbrowser
from textPlay.colors import *
from textPlay.options import options
from textPlay.Gsearch import g_search
from textPlay.morse import Morse

pt = 'TP>> '

# COLORS
red = RED
green = GREEN
blue = BLUE
yellow = YELLOW
magenta = MAGENTA
cyan = CYAN
reset = RESET
lit_red = LIGHT_RED


@click.group()
def textPlay_cli():
    click.echo("\n\tTextPlay CLI\n")
    pass

# MENU
@click.command()
def menu():
    options([(f'Web Search {RESET}', lambda: search()),
             (f'Morse Code/Decode {RESET}', lambda: morse()),
             (f'Text Play Tools {RESET}', lambda: tp_tools()),
             (f'Source Code {RESET}', lambda: source_code())],
             index=f"{magenta}>",
             head = "\n\tTextPlay CLI\n")

# SEARCH
@click.command()
@click.option('--search','-s', prompt=f'{pt}Search...', help="Search query")
@click.option('--result','-r', prompt=f'{pt}Number of results', help="Number of results", default=1)
def search(search, result):
    print(f"{pt}Searching for: {search}")
    print(f"{pt}Search results ↓\n{pt}{g_search(search, result)}")

# TODO: CLI -> Error: Got unexpected extra argument (menu)

# MORSE
@click.command()
@click.option('--input_text', '-i', prompt='Enter text/Morse code', help="Text or Morse code")
def morse(input_text):
    print("Received input:", input_text)  # Debug statement to verify input
    
    morse_instance = Morse()
    
    if "/" in input_text:
        decoded_text = morse_instance.decoder(input_text)
        click.echo(f"Decoded Text: {decoded_text}")
    else:
        encoded_text = morse_instance.coder(input_text)
        click.echo(f"Encoded Morse Code: {encoded_text + " /"}")
        
def tp_tools():
    tools = f"""
\t{LIGHT_YELLOW}Text Play Tools{RESET}

{BOLD}• Web Search {RESET}
    This tool will search Google for a query and display the results.
    you can specify the number of results to display.

{BOLD}• Morse Code/Decode {RESET}
    This tool will convert text to morse code and vice versa.
    It will automatically detect if the input is morse code or text.

{BOLD}• Box {RESET}
    This tool will print a box with a message and a title with specified length.

{BOLD}• Colors {RESET}
    This tool will print text with different colors and styles.

{BOLD}• Options {RESET}
    This tool will display a menu with options and handle user input for navigation and selection.

{BOLD}• Password Generator {RESET}
    This tool will generate a random password with the specified length.

{BOLD}• Progress Bar {RESET}
    This tool will display a progress bar with a specified terminal length.

{BOLD}• Encryption Animation {RESET}
    This tool will display an encryption animation in the terminal with a specified word.

{BOLD}• Source Code {RESET}
    View our source code at github. {BRIGHT_BLUE}https://github.com/rakeshkanna-rk/textPlay{RESET}
    Author: {MAGENTA}Rakesh Kanna S{reset}
"""

    print(tools)


def source_code():
    print(f"Source code at: {BRIGHT_BLUE}https://github.com/rakeshkanna-rk/textPlay{RESET}")
    webbrowser.open('https://github.com/rakeshkanna-rk/textPlay')
    print(f"Auto opening browser...{GREEN} ✔{RESET}")


textPlay_cli.add_command(search)
textPlay_cli.add_command(morse)
textPlay_cli.add_command(menu)
