from paiza_scout_crawler import PaizaScoutCrawler
from mynavi_scout_crawler import MynaviScoutCrawler
from spreadsheet_writer import SpreadsheetWriter

def main():

    paiza_scout_crawler = PaizaScoutCrawler()
    paiza_scouts = paiza_scout_crawler.get_scouts()
    
    mynavi_scout_crawler = MynaviScoutCrawler()
    mynavi_scouts = mynavi_scout_crawler.get_scouts()

    scouts = paiza_scouts + mynavi_scouts

    """
    directory = "./tests/parse_paiza_format/test_case/"
    file_names = os.listdir(directory)
    in_files = [file_name for file_name in file_names if file_name.endswith(".in")]
    test_names = [file_name[:-3] for file_name in in_files]

    scouts = []
    for test_name in test_names:            
        with open(directory + test_name + '.in', 'r') as f:
            input = f.read()

        scouts.append(PaizaScoutParser.parse_scout(input))

    directory = "./tests/parse_mynavi_format/test_case/"
    file_names = os.listdir(directory)
    in_files = [file_name for file_name in file_names if file_name.endswith(".in")]
    test_names = [file_name[:-3] for file_name in in_files]

    for test_name in test_names:            
        with open(directory + test_name + '.in', 'r') as f:
            input = f.read()
        scouts.append(MynaviScoutParser.parse_scout(input))
    """

    spreadsheet_writer = SpreadsheetWriter("JobScout")
    spreadsheet_writer.write_scouts(scouts)

if __name__ == '__main__':
    main()