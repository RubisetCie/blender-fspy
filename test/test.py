import pathlib
import unittest
import importlib.util

# Load fSpy module without trigger the load of `__init__.py` which contains invalid `bpy` import.
fspy_path = pathlib.Path(__file__).resolve().parent.parent / 'fspy_blender_ng' / 'fspy.py'
fspy_spec = importlib.util.spec_from_file_location("fspy", fspy_path)
fspy = importlib.util.module_from_spec(fspy_spec)
fspy_spec.loader.exec_module(fspy)

def get_test_data(file_name: str) -> str:
    """Helper to get the path of test assets"""
    return pathlib.Path(__file__).parent / file_name

class TestfSpyProjectLoading(unittest.TestCase):
    def test_valid_project(self):
        """
        Opening a valid project should not raise
        """
        fspy.Project(get_test_data('canon5d_16mm.fspy'))

    def test_wrong_project_version(self):
        """
        Opening projects with an unsupported binary version should fail
        """
        with self.assertRaises(fspy.ParseError):
            fspy.Project(get_test_data('invalid_project_version.fspy'))

    def test_invalid_file_type(self):
        """
        Opening files that are not fSpy project files should fail
        """
        with self.assertRaises(fspy.ParseError):
            fspy.Project(get_test_data('json_export.json'))

if __name__ == '__main__':
    unittest.main()