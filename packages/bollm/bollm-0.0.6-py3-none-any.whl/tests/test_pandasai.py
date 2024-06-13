import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import pandas as pd

# Importing the functions from the main script
from bollm.pandasai import extract_code_from_log, st_redirect, st_stdout, get_file_ext, parse_response

class TestPandasaiFunctions(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="Code running:\n\n```\nprint('Hello, World!')\n```")
    def test_extract_code_from_log(self, mock_file):
        file_path = "dummy_path"
        expected_output = "print('Hello, World!')\n"
        result = extract_code_from_log(file_path)
        self.assertEqual(result, expected_output)

    def test_get_file_ext(self):
        self.assertEqual(get_file_ext("example.png"), ".png")
        self.assertEqual(get_file_ext("example.txt"), ".txt")
        self.assertEqual(get_file_ext("example"), "")

    @patch("streamlit.markdown")
    @patch("streamlit.table")
    @patch("streamlit.image")
    def test_parse_response(self, mock_image, mock_table, mock_markdown):
        # Test with integer
        parse_response(42)
        mock_markdown.assert_called_with(42)

        # Test with DataFrame
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        parse_response(df)
        mock_table.assert_called_with(df)

        # Test with string
        parse_response("Hello, World!")
        mock_markdown.assert_called_with("Hello, World!")

        # Test with image file
        parse_response("image.png")
        mock_image.assert_called_with("image.png")

        # Test with unrecognized type
        with self.assertRaises(NotImplementedError):
            parse_response(["unexpected", "type"])

if __name__ == '__main__':
    unittest.main()
