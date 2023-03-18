import sys
import unittest
import os
import json
file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(file_path + "/../..")
from mynavi_scaut_parser import MynaviScautParser

class TestParseMynaviScaut(unittest.TestCase):
    
    def test_parse_mynavi_scaut(self):
        directory = file_path + "/test_case"
        file_names = os.listdir(directory)
        in_files = [file_name for file_name in file_names if file_name.endswith(".in")]
        test_names = [file_name[:-3] for file_name in in_files]

        for test_name in test_names:            
            with open(file_path + "/test_case/" + test_name + '.in', 'r') as f:
                input = f.read()

            scaut = MynaviScautParser.parse_scaut(input)

            with open(file_path + "/test_case/" + test_name + '.out', 'r') as f:
                expected_output =  json.loads(f.read())
            self.assertEqual(scaut.to_dict(), expected_output)

if __name__ == '__main__':
    unittest.main()
