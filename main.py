from paiza_scaut_crawler import PaizaScautCrawler
from paiza_scaut_parser import PaizaScautParser
from mynavi_scaut_crawler import MynaviScautCrawler

def main():

    paiza_scaut_crawler = PaizaScautCrawler()
    scauts = paiza_scaut_crawler.get_scauts()

    mynavi_scaut_crawler = MynaviScautCrawler()
    scauts = mynavi_scaut_crawler.get_scauts()

    
    for scaut in scauts:
        print(scaut)

if __name__ == '__main__':
    main()