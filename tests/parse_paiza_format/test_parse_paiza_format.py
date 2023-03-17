import sys
sys.path.append("../..")
from paiza_scaut_parser import PaizaScautParser
import unittest
import os
import json

class TestParsePaizaScaut(unittest.TestCase):
    
    def test_parse_paiza_scaut(self):
        directory = "test_case"
        file_names = os.listdir(directory)
        in_files = [file_name for file_name in file_names if file_name.endswith(".in")]
        test_names = [file_name[:-3] for file_name in in_files]

        for test_name in test_names:            
            with open("test_case/" + test_name + '.in', 'r') as f:
                input = f.read()

            with open("test_case/" + test_name + '.out', 'r') as f:
                expected_output =  json.loads(f.read())

            scaut = PaizaScautParser.parse_scaut(input)

            self.assertEqual(scaut, expected_output)

if __name__ == '__main__':
    unittest.main()
