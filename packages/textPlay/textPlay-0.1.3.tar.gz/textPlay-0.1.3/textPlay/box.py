import shutil

def create_box(title, content, width_percentage):
    """
    Create a box with a title and content to display in the terminal.

    Parameters:
    title (str): The title to display at the top of the box.
    content (list of str): The content lines to display inside the box.
    width_percentage (int): The width of the box as a percentage of the terminal width.

    Returns:
    str: The formatted box with the title and content as a string.

    Example:
    >>> title = "Title"
    >>> content = ["word 1", "word 2"]
    >>> width_percentage = 99  # Adjust as needed
    >>> box_with_title = create_box(title, content, width_percentage)
    >>> print(box_with_title)
    ╭─ Title ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ word 1                                                                                                                     │
    │ word 2                                                                                                                     │
    ╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    """
    terminal_width = shutil.get_terminal_size().columns
    box_width = int(terminal_width * width_percentage / 100)

    box_top = f"╭─ {title} {'─' * (box_width - len(title) - 4)}╮"
    lines = [box_top]
    for line in content:
        lines.append(f"│ {line.ljust(box_width - 3)} │")
    box_bottom = f"╰{'─' * (box_width - 1)}╯"

    lines.append(box_bottom)
    return "\n".join(lines)
