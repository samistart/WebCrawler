from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import urlopen
from config import *
from file_writing import *
from urllib.request import urlretrieve
from multiprocessing.dummy import Pool
import urllib.parse

scraped = set()


def scrape(url, domain_name):
    soup = BeautifulSoup(urlopen(url).read(), "html.parser")
    assets = [i.get('src') for i in soup.find_all() if i.get('src')]
    for asset in assets:
        parse = urlparse(asset)
        if parse.netloc == '' or parse.netloc == domain_name:
            path = parse.path
            location = urllib.parse.urljoin(BASE_URL, parse.path)
            try:
                if location not in scraped:
                    file_path = PROJECT_NAME + parse.path
                    create_dir_from_file_path(file_path)
                    if not os.path.isfile(file_path):
                        urlretrieve(location, file_path)    #todo use asynchronous io
                        scraped.add(location)
            except:
                print("Cannot download asset: " + asset)
                scraped.add(location)


def get_links(url, base_url):
    links = set()
    soup = BeautifulSoup(urlopen(url).read(), "html.parser")
    for a in soup.find_all('a', href=True):
        link = base_url + a['href']
        links.add(link)
    return links




