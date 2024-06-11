import unittest
from unittest.mock import patch
import os
import json
import argparse  # Add this line
from find_and_replace import main

class TestMain(unittest.TestCase):

    def setUp(self):
        self.filename = 'test.txt'
        with open(self.filename, 'w') as f:
            f.write('Hello, World!')

    def tearDown(self):
        os.remove(self.filename)

    def test_replace_in_file(self):
        main.replace_in_file(self.filename, 'World', 'GitHub Copilot')
        with open(self.filename, 'r') as f:
            self.assertEqual(f.read(), 'Hello, GitHub Copilot!')

    def test_replace_in_file_no_match(self):
        main.replace_in_file(self.filename, 'No Match', 'GitHub Copilot')
        with open(self.filename, 'r') as f:
            self.assertEqual(f.read(), 'Hello, World!')

    @patch('argparse.ArgumentParser.parse_args')
    def test_main_replace_from_file(self, mock_args):
        mock_args.return_value = argparse.Namespace(file=self.filename, read_from_file=True)
        with open('.project-properties.json', 'w') as f:
            json.dump([{'search': 'World', 'replacement': 'GitHub Copilot'}], f)
        main.main()
        with open(self.filename, 'r') as f:
            self.assertEqual(f.read(), 'Hello, GitHub Copilot!')
        os.remove('.project-properties.json')

    @patch('argparse.ArgumentParser.parse_args')
    def test_main_replace_from_args(self, mock_args):
        mock_args.return_value = argparse.Namespace(file=self.filename, search='World', replacement='GitHub Copilot', read_from_file=False)
        main.main()
        with open(self.filename, 'r') as f:
            self.assertEqual(f.read(), 'Hello, GitHub Copilot!')

if __name__ == '__main__':
    unittest.main()