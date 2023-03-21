import os
import json
from paiza_scout_crawler import PaizaScoutCrawler
from mynavi_scout_crawler import MynaviScoutCrawler
from spreadsheet_writer import SpreadsheetWriter

def main():

    file_path = os.path.abspath(os.path.dirname(__file__))
    with open(file_path + "/private/settings.json", 'r') as f:
        settings =  json.loads(f.read())

    if settings["load_paiza"]:
        paiza_scout_crawler = PaizaScoutCrawler()
        paiza_scouts = paiza_scout_crawler.get_scouts()
    else:
        paiza_scouts = []

    if settings["load_mynavi"]:
        mynavi_scout_crawler = MynaviScoutCrawler()
        mynavi_scouts = mynavi_scout_crawler.get_scouts()
    else:
        mynavi_scouts = []

    scouts = paiza_scouts + mynavi_scouts

    spreadsheet_writer = SpreadsheetWriter(settings["spread_sheet_name"], settings["work_sheet_name"])
    spreadsheet_writer.write_scouts(scouts)

if __name__ == '__main__':
    main()