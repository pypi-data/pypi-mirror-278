import unittest
import tempfile
import time
import shutil
import os
from RootWhiz.app.RootWhiz import RootWhiz


def _retry_remove_directory(path, retries=5, delay=1):
    """
    Retry removing a directory with a delay in case of PermissionError.
    """
    for i in range(retries):
        try:
            shutil.rmtree(path)
            break
        except PermissionError as e:
            print(f"Error removing directory (attempt {i + 1}): {e}")
            time.sleep(delay)


class TestRootWhiz(unittest.TestCase):
    def setUp(self):
        """
        Set up a temporary directory structure for testing.
        """
        self.test_dir = tempfile.mkdtemp()
        self.marker_file = '.gitignore'
        self.marker_file_path = os.path.join(self.test_dir, self.marker_file)

        # Create the marker file in the temporary directory
        with open(self.marker_file_path, 'w') as f:
            f.write('marker')

    def tearDown(self):
        """
        Clean up the temporary directory structure after tests.
        """
        _retry_remove_directory(self.test_dir)

    def test_find_project_root(self):
        """
        Test if the RootWhiz correctly identifies the project root.
        """
        os.chdir(self.test_dir)
        pilot = RootWhiz(self.marker_file)
        self.assertEqual(pilot.get_project_root(), self.test_dir)

    def test_set_project_root(self):
        """
        Test if the RootWhiz can set a new project root.
        """
        os.chdir(self.test_dir)
        pilot = RootWhiz(self.marker_file)

        # Create a new directory to set as project root
        new_root = tempfile.mkdtemp()
        new_marker_file_path = os.path.join(new_root, self.marker_file)
        with open(new_marker_file_path, 'w') as f:
            f.write('marker')

        result = pilot.set_project_root(new_root)
        self.assertTrue(result)
        self.assertEqual(pilot.get_project_root(), new_root)

        # Clean up the new temporary directory
        _retry_remove_directory(new_root)

    def test_reset_project_root(self):
        """
        Test if the RootWhiz can reset the project root.
        """
        os.chdir(self.test_dir)
        pilot = RootWhiz(self.marker_file)

        # Change to a subdirectory
        sub_dir = os.path.join(self.test_dir, 'sub_dir')
        os.makedirs(sub_dir)
        os.chdir(sub_dir)

        # Ensure the project root is still correct
        self.assertEqual(pilot.get_project_root(), self.test_dir)

        # Remove the marker file and reset project root
        os.remove(self.marker_file_path)
        result = pilot.reset_project_root()
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
