from pathlib import Path
from re import sub
from shlex import quote
import os

def filename_with_suffix(filename: str, suffix: str) -> str:
  return Path(filename).stem + '.' + suffix

def sanitize_input(user_input: str) -> str:
    if os.name == 'posix':
        # Sanitize for POSIX command line
        sanitized_input = quote(user_input)
        # Remove invalid filename characters for POSIX (if any)
        sanitized_input = sub(r'[:]', '', sanitized_input)
    elif os.name == 'nt':
        # Define a regex pattern for potentially dangerous characters for Windows CMD
        dangerous_chars = r'[&|;^<>()%]'
        # Replace dangerous characters with an empty string
        sanitized_input = sub(dangerous_chars, '', user_input)
        # Enclose the sanitized input in double quotes
        sanitized_input = f'"{sanitized_input}"'
        # Define a regex pattern for invalid filename characters on Windows
        invalid_filename_chars = r'[\\/:"*?<>|]'
        # Remove invalid filename characters
        sanitized_input = sub(invalid_filename_chars, '', sanitized_input)
    else:
        raise NotImplementedError("Unsupported operating system")

    return sanitized_input