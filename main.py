from config import *
from crawler import Crawler
from urllib.request import urlopen
from scraping import *


def main():
    crawler = Crawler(PROJECT_NAME, BASE_URL, True)
    for _ in range(NUMBER_OF_THREADS - 1):
        crawler = Crawler(PROJECT_NAME, BASE_URL, False)

main()
