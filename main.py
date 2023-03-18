from paiza_scaut_crawler import PaizaScautCrawler
from paiza_scaut_parser import PaizaScautParser
from mynavi_scaut_crawler import MynaviScautCrawler
from mynavi_scaut_parser import MynaviScautParser

def main():

    paiza_scaut_crawler = PaizaScautCrawler()
    paiza_scauts = paiza_scaut_crawler.get_scauts()

    """
    mynavi_scaut_crawler = MynaviScautCrawler()
    mynavi_scauts = mynavi_scaut_crawler.get_scauts()
    """

if __name__ == '__main__':
    main()