import os
from RootWhiz.utils.path_util import PathUtils


class RootWhiz:
    def __init__(self, marker_file='project_marker.txt'):
        """
        Initializes the RootWhiz instance and attempts to find the project root.

        Args:
            marker_file (str): The name of the marker file to look for. Defaults to 'project_marker.txt'.
        """
        self.marker_file = marker_file
        self.project_root = PathUtils.find_project_root(marker_file)
        if self.project_root:
            print(f"Project root found at: {self.project_root}")
        else:
            print("Project root not found.")

    def get_project_root(self):
        """
        Returns the path to the project root directory if found.

        Returns:
            str: The path to the project root directory if the marker file is found, otherwise None.
        """
        return self.project_root

    def set_project_root(self, new_root):
        """
        Allows setting a new project root directory manually.

        Args:
            new_root (str): The new path to set as the project root.

        Returns:
            bool: True if the new root is set successfully, False otherwise.
        """
        if os.path.isdir(new_root) and self.marker_file in os.listdir(new_root):
            self.project_root = new_root
            print(f"Project root manually set to: {new_root}")
            return True
        else:
            print(f"Failed to set project root to: {new_root}. Ensure it is a directory containing {self.marker_file}.")
            return False

    def reset_project_root(self):
        """
        Resets the project root by searching for the marker file again.

        Returns:
            str: The path to the project root directory if the marker file is found, otherwise None.
        """
        self.project_root = PathUtils.find_project_root(self.marker_file)
        if self.project_root:
            print(f"Project root reset to: {self.project_root}")
        else:
            print("Project root not found after reset.")
        return self.project_root
