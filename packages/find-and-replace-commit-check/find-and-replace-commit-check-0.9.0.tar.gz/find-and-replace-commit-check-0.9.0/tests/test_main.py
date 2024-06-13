# import unittest
# from find_and_replace.main import replace_in_file, main
# class TestMainFunctions(unittest.TestCase):
#     def test_replace_in_file(self):
#         pass  # TODO: Write your test here

#     def test_main(self):
#         pass  # TODO: Write your test here

# if __name__ == '__main__':
#     unittest.main()

import unittest
import argparse
from unittest.mock import patch, mock_open
from find_and_replace.main import replace_in_file, main

class TestMainFunctions(unittest.TestCase):
    @patch('fileinput.FileInput')
    def test_replace_in_file(self, mock_fileinput):
        """
        This test checks if the replace_in_file function correctly opens the file and replaces the specified text.
        """
        # Mock the file input to return a specific line of text
        mock_fileinput.return_value.__enter__.return_value = ['hello world']
        # Call the function with a specific search and replacement
        replace_in_file('dummy.txt', 'hello', 'hi')
        # Assert that the file was opened correctly
        mock_fileinput.assert_called_once_with('dummy.txt', inplace=True)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('find_and_replace.main.replace_in_file')
    @patch('os.getcwd', return_value='/dummy/path')
    @patch('builtins.open', new_callable=mock_open, read_data='{"search": "hello", "replacement": "hi"}')
    @patch('json.load', return_value=[{"search": "hello", "replacement": "hi"}])
    def test_main(self, mock_json_load, mock_open, mock_getcwd, mock_replace_in_file, mock_parse_args):
        """
        This test checks if the main function correctly reads the configuration file and calls the replace_in_file function with the correct arguments.
        """
        # Mock the command line arguments
        mock_parse_args.return_value = argparse.Namespace(files=['dummy.txt'], find=None, replacement=None, read_from_file=True, config='.find-and-replace.json')
        # Call the main function
        main()
        # Assert that the config file was opened correctly and the replace_in_file function was called with the correct arguments
        mock_open.assert_called_once_with('/dummy/path/.find-and-replace.json', 'r')
        mock_replace_in_file.assert_called_once_with('dummy.txt', 'hello', 'hi')

if __name__ == '__main__':
    unittest.main()


