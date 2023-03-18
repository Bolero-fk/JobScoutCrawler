from paiza_scaut_crawler import PaizaScautCrawler
from mynavi_scaut_crawler import MynaviScautCrawler
from mynavi_scaut_parser import MynaviScautParser
from spreadsheet_writer import SpreadsheetWriter
import os

def main():

    paiza_scaut_crawler = PaizaScautCrawler()
    paiza_scauts = paiza_scaut_crawler.get_scauts()

    mynavi_scaut_crawler = MynaviScautCrawler()
    mynavi_scauts = mynavi_scaut_crawler.get_scauts()

    scauts = paiza_scauts + mynavi_scauts

    """
    directory = "./tests/parse_paiza_format/test_case/"
    file_names = os.listdir(directory)
    in_files = [file_name for file_name in file_names if file_name.endswith(".in")]
    test_names = [file_name[:-3] for file_name in in_files]

    scauts = []
    for test_name in test_names:            
        with open(directory + test_name + '.in', 'r') as f:
            input = f.read()

        scauts.append(PaizaScautParser.parse_scaut(input))

    directory = "./tests/parse_mynavi_format/test_case/"
    file_names = os.listdir(directory)
    in_files = [file_name for file_name in file_names if file_name.endswith(".in")]
    test_names = [file_name[:-3] for file_name in in_files]

    for test_name in test_names:            
        with open(directory + test_name + '.in', 'r') as f:
            input = f.read()
        scauts.append(MynaviScautParser.parse_scaut(input))
    """

    spreadsheet_writer = SpreadsheetWriter("JobScout")
    spreadsheet_writer.write_scauts(scauts)

if __name__ == '__main__':
    main()