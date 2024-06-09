"""
file.py
"""

import os
import shutil

class ClearDirectoryError(Exception):
    """Custom exception for errors encountered while clearing a directory."""

def clear_directory(directory):
    """
    Clears all files and subdirectories within the specified directory.

    This function checks if the specified directory exists. If it does, it removes the entire
    directory and its contents. If an error occurs during the deletion process, a ClearDirectoryError
    is raised with the appropriate message.

    If the directory does not exist, the function silently completes without performing any action.

    Parameters:
    directory (str): The path of the directory to clear.
    """
    if os.path.exists(directory):
        try:
            shutil.rmtree(directory)
        except Exception as e:
            raise ClearDirectoryError(f'Failed to clear the directory {directory}. Reason: {e}') from e

class CreateDirectoryError(Exception):
    """Custom exception for errors related to directory creation."""
    def __init__(self, path, message="Failed to create directory"):
        self.path = path
        self.message = f"{message}: {path}"
        super().__init__(self.message)

def create_directory(path):
    """
    Creates a directory if it doesn't already exist.

    Parameters:
    path (str): The path of the directory to create.

    Raises:
    DirectoryCreationError: If an error occurs during directory creation.

    Returns:
    None
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        raise CreateDirectoryError(path, str(e)) from e
