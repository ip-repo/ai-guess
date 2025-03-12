import shutil
import sys
SYSTEM_MESSAGE = """
You are given a file path (or directory) as input. Your task is to:
1. Analyze the file path and determine the likely usage of the file based on common file types and extensions and names.
2. Assess whether the file is potentially risky based on its extension or known patterns associated with harmful files (e.g., executable files, scripts, etc.).
"""


def get_terminal_width() -> None:
    """
    Retrieves the width of the terminal window.
        - Uses shutil.get_terminal_size to fetch the terminal dimensions.
        - Applies a fallback size of (80, 20) if the terminal size is unavailable.

    Returns:
        int: The number of columns (width) of the terminal window. 
             Defaults to 80 if the terminal size cannot be determined.
    
   
    
    """
    columns, rows = shutil.get_terminal_size(fallback=(80, 20))
    return columns

def signal_handler(sig, frame):
    """
    Handles an interrupt signal (e.g., Ctrl+C) to gracefully terminate the program.
        - Prints a message indicating that the program was interrupted by the user.
        - Exits the program with a status code of 0, indicating a clean termination.

    Args:
        sig: The signal number received (e.g., SIGINT).
        frame: The current stack frame when the signal was received.

    """
    print("\nInterrupted by user. Exiting...")
    sys.exit(0)

