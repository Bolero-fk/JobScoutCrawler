import sys
sys.path.append("../..")
from mynavi_scaut_parser import MynaviScautParser
import unittest
import os
import json

class TestParseMynaviScaut(unittest.TestCase):
    
    def test_parse_mynavi_scaut(self):
        directory = "test_case"
        file_names = os.listdir(directory)
        in_files = [file_name for file_name in file_names if file_name.endswith(".in")]
        test_names = [file_name[:-3] for file_name in in_files]

        for test_name in test_names:            
            with open("test_case/" + test_name + '.in', 'r') as f:
                input = f.read()

            scaut = MynaviScautParser.parse_scaut(input)

            with open("test_case/" + test_name + '.out', 'r') as f:
                expected_output =  json.loads(f.read())
            self.assertEqual(scaut, expected_output)



if __name__ == '__main__':
    unittest.main()
