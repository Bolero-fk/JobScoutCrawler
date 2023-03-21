import sys
import unittest
import os
import json
file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(file_path + "/../..")
from spreadsheet_writer import SpreadsheetWriter
from scout import Scout

class TestWriteSpreadsheet(unittest.TestCase):
    
    def test_write_spreadsheet(self):
        directory = file_path + "/test_case"
        file_names = os.listdir(directory)
        in_files = [file_name for file_name in file_names if file_name.endswith(".in")]
        test_names = [file_name[:-3] for file_name in in_files]

        for test_name in test_names:            
            with open(file_path + "/test_case/" + test_name + '.in', 'r') as f:
                scouts_json =  json.loads(f.read())
                scouts  = [Scout(                    
                    scout_json['company_name'], 
                    scout_json['min_salary'], 
                    scout_json['max_salary'], 
                    scout_json['location'], 
                    scout_json['using_lang'], 
                    scout_json['description'], 
                    scout_json['recieve_date'], 
                    scout_json['limit_day'],
                    scout_json['site_name']) for scout_json in scouts_json]


            spreadsheet_writer = SpreadsheetWriter("JobScout", "テスト用")
            spreadsheet_writer.write_scouts(scouts)

            with open(file_path + "/test_case/" + test_name + '.out', 'r') as f:
                expected_output =  json.loads(f.read())

            self.assertEqual(spreadsheet_writer.worksheet.get_all_values(), expected_output)
            spreadsheet_writer.worksheet.clear()

if __name__ == '__main__':
    unittest.main()
