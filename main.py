from paiza_scaut_crawler import PaizaScautCrawler
from paiza_scaut_parser import PaizaScautParser

def main():
    paiza_scaut_crawler = PaizaScautCrawler()
    scauts = paiza_scaut_crawler.get_scauts()

    for scaut in scauts:
        print(PaizaScautParser.parse_scaut(scaut))

if __name__ == '__main__':
    main()