# __init__.py

from .colors import *
from .Gsearch import g_search
from .morse import Morse
from .options import options
from .password_generator import create_password
from .encrypt_animation import encrypted


__all__ = [
    "g_search",
    "Morse",
    "options",
    "create_password",
    "encrypted",
]
