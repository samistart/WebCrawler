import config
from crawler import Crawler


def main():
    crawler = Crawler(config.PROJECT_NAME, config.BASE_URL, True)
    for _ in range(config.NUMBER_OF_THREADS - 1):
        crawler = Crawler(config.PROJECT_NAME, config.BASE_URL, False)


main()
