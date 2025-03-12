import shutil
import sys
SYSTEM_MESSAGE = """

You are given a file path as input. Your task is to:
1. Analyze the file path and determine the likely usage of the file based on common file types and extensions.
2. Assess whether the file is potentially risky based on its extension or known patterns associated with harmful files (e.g., executable files, scripts, etc.).
        
Example:

I've analyzed the file path and determined that it appears to be pointing to a Python script named check.py located in a directory structure as follows:

C:\\Users\\user\\Desktop\\ai-directory
|...
| check.py

Based on this, I would categorize the file as likely being an executable Python script. Here's why:

1. The file name starts with check, which is a common name for a Python script that performs some action.
2. The file path includes a directory structure (ai-directory) and another file (check.py), indicating that this is a nested folder structure.
3. The file extension is .py, which is the standard file extension for Python scripts.

However, I would also like to assess whether this file could potentially be risky based on its extension or known patterns associated with harmful files:

 'py': This is a common Python file extension, but it's not uncommon for malicious code to be embedded in Python scripts.
 '.py' extension: Some Python scripts can contain sensitive information or executable code that needs to be executed by the system. However, this also depends on the specific script and its intended use.

To further assess the risk, I would consider checking the following:

1. The file's contents for any suspicious code or data.
2. The file's permissions and access rights to ensure it can only be accessed by authorized users.
3. The file's history of modifications and who last modified it.

Based on this analysis, I would categorize the file as potentially executable Python script with some potential risk, but not necessarily malicious.

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

