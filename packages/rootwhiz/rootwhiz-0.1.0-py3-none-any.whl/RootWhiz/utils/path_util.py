import os


class PathUtils:
    @staticmethod
    def find_project_root(marker_file='project_marker.txt'):
        """
        Finds the root of the project by looking for a marker file.

        Args:
            marker_file (str): The name of the marker file to look for. Defaults to 'project_marker.txt'.

        Returns:
            str: The path to the project root directory if the marker file is found, otherwise None.
        """
        current_dir = os.getcwd()

        while current_dir != os.path.dirname(current_dir):
            if marker_file in os.listdir(current_dir):
                return current_dir
            current_dir = os.path.dirname(current_dir)

        return None
