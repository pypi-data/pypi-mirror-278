import random
import string

def create_password(length = 12):
    """
    Generate a random password with specified length.

    Parameters:
    length (int): The length of the password to generate. Default is 12.

    Returns:
    str: A randomly generated password consisting of uppercase letters, lowercase letters,
         digits, and special characters.

    Example:
    >>> generate_password()
    'Xz7F#bN@3kP6'
    >>> generate_password(length=20)
    'qG5$Y&z@v#2Sx7*r3B6p'
    """
    characters = string.ascii_letters + string.ascii_uppercase + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password
