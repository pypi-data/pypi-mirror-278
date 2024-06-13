# Text Colors
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'

# Bright Text Colors
BRIGHT_BLACK = '\033[90m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
BRIGHT_WHITE = '\033[97m'

# Background Colors
BG_BLACK = '\033[40m'
BG_RED = '\033[41m'
BG_GREEN = '\033[42m'
BG_YELLOW = '\033[43m'
BG_BLUE = '\033[44m'
BG_MAGENTA = '\033[45m'
BG_CYAN = '\033[46m'
BG_WHITE = '\033[47m'

# Bright Background Colors
BG_BRIGHT_BLACK = '\033[100m'
BG_BRIGHT_RED = '\033[101m'
BG_BRIGHT_GREEN = '\033[102m'
BG_BRIGHT_YELLOW = '\033[103m'
BG_BRIGHT_BLUE = '\033[104m'
BG_BRIGHT_MAGENTA = '\033[105m'
BG_BRIGHT_CYAN = '\033[106m'
BG_BRIGHT_WHITE = '\033[107m'

# Light (Bright) Text Colors
LIGHT_BLACK = '\033[90m'
LIGHT_RED = '\033[91m'
LIGHT_GREEN = '\033[92m'
LIGHT_YELLOW = '\033[93m'
LIGHT_BLUE = '\033[94m'
LIGHT_MAGENTA = '\033[95m'
LIGHT_CYAN = '\033[96m'
LIGHT_WHITE = '\033[97m'

# Light (Bright) Background Colors
BG_LIGHT_BLACK = '\033[100m'
BG_LIGHT_RED = '\033[101m'
BG_LIGHT_GREEN = '\033[102m'
BG_LIGHT_YELLOW = '\033[103m'
BG_LIGHT_BLUE = '\033[104m'
BG_LIGHT_MAGENTA = '\033[105m'
BG_LIGHT_CYAN = '\033[106m'
BG_LIGHT_WHITE = '\033[107m'


# Text Decorations
RESET = '\033[0m'
BOLD = '\033[1m'
DIM = '\033[2m'
ITALIC = '\033[3m'
UNDERLINE = '\033[4m'
BLINK = '\033[5m'
REVERSE = '\033[7m'
HIDDEN = '\033[8m'
STRIKETHROUGH = '\033[9m'

# Example usage
"""
print(f"{RED}This is red text{RESET}")
print(f"{BG_GREEN}This has a green background{RESET}")
print(f"{BOLD}This is bold text{RESET}")
print(f"{UNDERLINE}This is underlined text{RESET}")
print(f"{RED}This is red text{RESET}")
print(f"{BOLD}{UNDERLINE}{GREEN}Bold, underlined green text{RESET}")
"""