from bs4 import BeautifulSoup
from urllib.request import urlopen
from config import *
from file_writing import *
from urllib.request import urlretrieve
from multiprocessing.dummy import Pool

scraped = set()


def scrape(url):
    soup = BeautifulSoup(urlopen(url).read(), "html.parser")
    assets = [i.get('src') for i in soup.find_all() if i.get('src')]
    for asset in assets:
        parse = urlparse(asset)
        if parse.netloc == '' or parse.netloc == DOMAIN_NAME:
            try:
                path = parse.path
                if path[0] != '/':
                    path = "/" + path
                location = BASE_URL + parse.path
                if location not in scraped:
                    file_path = PROJECT_NAME + parse.path
                    create_dir_from_file_path(file_path)
                    if not os.path.isfile(file_path):
                        urlretrieve(location, file_path)    #todo use asynchronous io
                        scraped.add(location)
            except:
                print("Cannot find file.")



