from scraping import *
from urllib.request import urlparse
from file_writing import *
import threading
import time


class Crawler:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue = set()
    crawled = set()
    html_counter = 0
    initialised = False

    def __init__(self, project_name, base_url, is_first):
        Crawler.project_name = project_name
        Crawler.base_url = base_url
        Crawler.domain_name = urlparse(base_url).netloc
        self.start_time = time.monotonic()
        if is_first:
            self.init_queue_and_crawled()
            self.start_thread()
        else:
            while not Crawler.initialised:
                time.sleep(5)
                self.start_thread()

    def loop(self):
        while len(Crawler.queue) != 0:
            page_url = Crawler.queue.pop()
            self.crawl(page_url)
            Crawler.initialised = True
        print(str(time.monotonic() - self.start_time) + "seconds taken to crawl " + str(len(Crawler.crawled)) + "pages.")

    def start_thread(self):
        t = threading.Thread(target=self.loop)
        t.start()

    @staticmethod
    def init_queue_and_crawled():
        create_dir(Crawler.project_name)
        Crawler.queue = set()
        Crawler.queue.add(Crawler.base_url)
        Crawler.crawled = set()

    @staticmethod
    def crawl(page_url):
        if page_url not in Crawler.crawled:
            print('Now crawling ' + page_url)
            print('Queue ' + str(len(Crawler.queue)) + ' | Crawled  ' + str(len(Crawler.crawled)))
            links = Crawler.gather_links(page_url)
            Crawler.add_links_to_queue(links)
            Crawler.crawled.add(page_url)

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            url_info = urlparse(page_url)
            if url_info.netloc != Crawler.domain_name:
                return set()
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                soup = BeautifulSoup(html_bytes, "html.parser")
                file_path = get_file_path(Crawler.project_name, page_url)
                create_dir_from_file_path(file_path)
                write_file(file_path, html_string)
                scrape(soup, Crawler.domain_name)
                links = get_links(soup, Crawler.base_url)
                return links
            else:
                file_path = get_file_path(Crawler.project_name, page_url)
                create_dir_from_file_path(file_path)
                asynchronous_url_retrieve(page_url, file_path)
        except:
            print('Unable to crawl: ' + page_url)
            return set()

    @staticmethod
    def add_links_to_queue(links):
        if links is not None:
            for link in links:
                if link in Crawler.queue:
                    continue
                if link in Crawler.crawled:
                    continue
                if Crawler.domain_name not in link:
                    continue
                Crawler.queue.add(link)

