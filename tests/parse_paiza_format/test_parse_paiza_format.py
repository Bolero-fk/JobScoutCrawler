import sys
import unittest
import os
import json
file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(file_path + "/../..")
from paiza_scout_parser import PaizaScoutParser

class TestParsePaizaScout(unittest.TestCase):
    
    def test_parse_paiza_scout(self):
        directory = file_path + "/test_case"
        file_names = os.listdir(directory)
        in_files = [file_name for file_name in file_names if file_name.endswith(".in")]
        test_names = [file_name[:-3] for file_name in in_files]

        for test_name in test_names:            
            with open(file_path + "/test_case/" + test_name + '.in', 'r') as f:
                input = f.read()

            scout = PaizaScoutParser.parse_scout(input)

            with open(file_path + "/test_case/" + test_name + '.out', 'r') as f:
                expected_output =  json.loads(f.read())

            # remaining_daysは実行時の日時によって変わるのでそれぞれの結果からremaining_daysを除外した辞書を作成する
            output_without_remaining_days = {k: v for k, v in scout.to_dict().items() if k not in  ["remaining_days"]}
            expected_output_without_remaining_days = {k: v for k, v in expected_output.items() if k not in  ["remaining_days"]}

            self.assertEqual(output_without_remaining_days, expected_output_without_remaining_days)

if __name__ == '__main__':
    unittest.main()
