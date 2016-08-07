from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import urlopen
from config import *
from file_writing import *
from multiprocessing.dummy import Pool
import urllib.parse

scraped = set()


def scrape(soup, domain_name):
    for asset in [i.get('src') for i in soup.find_all() if i.get('src')]:
        parse = urllib.parse.urlparse(asset)
        if parse.netloc == '' or parse.netloc == domain_name:
            path = parse.path
            location = urllib.parse.urljoin(BASE_URL, parse.path)
            try:
                if location not in scraped:
                    file_path = PROJECT_NAME + parse.path
                    create_dir_from_file_path(file_path)
                    if not os.path.isfile(file_path):
                        asynchronous_url_retrieve(location, file_path)
                        scraped.add(location)
            except:
                print("Cannot download asset: " + asset)
                scraped.add(location)


def get_links(soup, base_url):
    links = set()
    for a in soup.find_all('a', href=True):
        link = base_url + a['href']
        links.add(link)
    return links




