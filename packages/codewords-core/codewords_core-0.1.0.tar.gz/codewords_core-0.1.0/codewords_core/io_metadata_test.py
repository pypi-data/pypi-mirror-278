import unittest

from codewords_core.io_metadata import (
    JsonSchemaLite,
    concrete_file_paths,
    get_with_path,
    paths_to_filenames,
    set_at_path,
)


class TestJsonSchemaLite(unittest.TestCase):
    def test_paths_to_file_types(self):
        schema_dict = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "object",
                        "format": "csv",
                        "properties": {
                            "filename": {"type": "string"},
                            "content": {"type": "string"}
                        }
                    },
                    "other": {"type": "string"}
                }
            }
        }

        schema = JsonSchemaLite.parse_obj(schema_dict)

        # Collect all paths to file types
        paths = list(schema.paths_to_file_types())

        # Expected to find path to the 'file' under items of the root array
        expected_paths = [(None, 'file')]
        self.assertEqual(paths, expected_paths, "The paths to file types do not match expected paths.")


class TestDictPathUtilities(unittest.TestCase):

    def test_concrete_file_paths(self):
        # Test on a nested dictionary with list items
        input_value = {
            "files": [
                {"file": {"filename": "file1.txt", "contents": "data1"}},
                {"file": {"filename": "file2.txt", "contents": "data2"}}
            ]
        }
        dict_path = (None, 'file')
        expected_output = [(0, 'file'), (1, 'file')]
        self.assertEqual(
            concrete_file_paths(dict_path, input_value['files']),
            expected_output,
            "concrete_file_paths did not return expected paths for lists"
        )

    def test_get_with_path(self):
        # Test getting a nested value
        obj = {
            "a": {
                "b": {
                    "c": 10
                }
            }
        }
        path = ('a', 'b', 'c')
        self.assertEqual(
            get_with_path(obj, path),
            10,
            "get_with_path did not return the correct nested value"
        )

        # Test exception on invalid path element (None)
        with self.assertRaises(ValueError):
            get_with_path(obj, ('a', None, 'c'))

    def test_set_at_path(self):
        # Test setting a nested value
        obj = {"a": {"b": {"c": 10}}}
        set_at_path(obj, ('a', 'b', 'c'), 20)
        self.assertEqual(obj['a']['b']['c'], 20, "set_at_path did not correctly set the nested value")

        # Test setting a new key in the object
        set_at_path(obj, ('a', 'b', 'd'), 30)
        self.assertEqual(obj['a']['b']['d'], 30, "set_at_path did not correctly set a new nested value")

        # Test exception on empty path
        with self.assertRaises(ValueError):
            set_at_path(obj, (), "no path")

        # Test exception on non-existent path leading to key error
        with self.assertRaises(KeyError):
            set_at_path(obj, ('x', 'y'), "invalid path")

    def test_paths_to_filenames(self):
        # Define a sample JSON schema that includes file types
        json_schema_dict = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "object",
                        "format": "pdf",
                        "properties": {
                            "filename": {"type": "string"},
                            "content": {"type": "string"}
                        }
                    },
                    "other": {"type": "string"}
                }
            }
        }
        json_schema = JsonSchemaLite.parse_obj(json_schema_dict)

        # Define a sample input dictionary matching the schema
        input_dict = {
            "files": [
                {"file": "report1.pdf"},
                {"file": "report2.pdf"}
            ]
        }

        # Expected output is paths to filenames
        expected = {
            (0, 'file'): "report1.pdf",
            (1, 'file'): "report2.pdf"
        }

        result = paths_to_filenames(json_schema, input_dict['files'])
        self.assertEqual(result, expected, "paths_to_filenames did not return the expected paths to filenames mapping")


if __name__ == '__main__':
    unittest.main()
