# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch, mock_open
import os
import json
import argparse
from find_and_replace.main import replace_in_file, main

class TestMain(unittest.TestCase):

    def setUp(self):
        self.filename = 'test.txt'
        with open(self.filename, 'w') as f:
            f.write('Hello, World!')

    def tearDown(self):
        os.remove(self.filename)

    # Test case: Basic functionality with a match in the file
    def test_replace_in_file(self):
        replace_in_file(self.filename, 'World', 'find and replace')
        with open(self.filename, 'r') as f:
            self.assertEqual(f.read(), 'Hello, find and replace!')

    # Test case: No match in the file
    def test_replace_in_file_no_match(self):
        replace_in_file(self.filename, 'No Match', 'find and replace')
        with open(self.filename, 'r') as f:
            self.assertEqual(f.read(), 'Hello, World!')

    # Test case: Replacement string contains special characters
    def test_replace_in_file_special_characters(self):
        replace_in_file(self.filename, 'World', 'find and replace!@#$%^&*()')
        with open(self.filename, 'r') as f:
            self.assertEqual(f.read(), 'Hello, find and replace!@#$%^&*()!')

    # Test case: Replacements are read from a file
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_replace_from_file(self, mock_args):
        mock_args.return_value = argparse.Namespace(files=[self.filename], read_from_file=True)
        with open('.project-properties.json', 'w') as f:
            json.dump([{'search': 'World', 'replacement': 'find and replace'}], f)
        main()
        with open(self.filename, 'r') as f:
            self.assertEqual(f.read(), 'Hello, find and replace!')
        os.remove('.project-properties.json')

    # Test case: Replacements are provided as arguments
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_replace_from_args(self, mock_args):
        mock_args.return_value = argparse.Namespace(files=[self.filename], search='World', replacement='find and replace', read_from_file=False)
        main()
        with open(self.filename, 'r') as f:
            self.assertEqual(f.read(), 'Hello, find and replace!')

    # Test case: Replacements are provided as arguments, replacement string contains special characters
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_replace_from_args_special_characters(self, mock_args):
        mock_args.return_value = argparse.Namespace(files=[self.filename], search='World', replacement='find and replace!@#$%^&*()', read_from_file=False)
        main()
        with open(self.filename, 'r') as f:
            self.assertEqual(f.read(), 'Hello, find and replace!@#$%^&*()!')

    # Test case: Replacements are read from a file, but the file does not exist
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_replace_from_file_no_file(self, mock_args):
        mock_args.return_value = argparse.Namespace(files=['non_existent_file.txt'], read_from_file=True)
        with open('.project-properties.json', 'w') as f:
            json.dump([{'search': 'World', 'replacement': 'find and replace'}], f)
        with self.assertRaises(FileNotFoundError):
            main()
        os.remove('.project-properties.json')

    # Test case: Replacement string contains a double quote
    def test_replace_in_file_double_quote(self):
        replace_in_file(self.filename, 'World', 'find and "replace"')
        with open(self.filename, 'r') as f:
            self.assertEqual(f.read(), 'Hello, find and "replace"!')

if __name__ == '__main__':
    unittest.main()
