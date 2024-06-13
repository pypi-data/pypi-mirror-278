"""
This module contains functions to encode text using some common ciphers, along with some custom ciphers.
"""

def Caesar(message, key):
    """
    Applies the Caesar cipher to the given message using the specified key.

    Args:
        message (str): The message to be encoded.
        key (int): The key to shift the characters by.

    Returns:
        str: The encoded message.

    """
    message = message.upper()
    str_result = ""

    for char in message:
        if char.isalpha():
            n = ord(char)
            n -= 65
            n = ((n + key) % 26)
            n += 65
            str_result += chr(n)
        else:
            str_result += char
    return str_result