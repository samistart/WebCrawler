import scraping
import bs4
import urllib.request
import file_writing
import threading
import time
import config
from xml_writer import XmlWriter


class Crawler:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue = set()
    crawled = set()
    html_counter = 0
    initialised = False
    xml_writer = None

    def __init__(self, project_name, base_url, is_first):
        Crawler.project_name = project_name
        Crawler.base_url = base_url
        Crawler.domain_name = urllib.request.urlparse(base_url).netloc
        Crawler.xml_writer = XmlWriter(project_name)
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
        file_writing.create_dir(Crawler.project_name)
        Crawler.queue = set()
        Crawler.queue.add(Crawler.base_url)
        Crawler.crawled = set()

    @staticmethod
    def crawl(page_url):
        if page_url not in Crawler.crawled:
            if config.LOGGING:
                print('Now crawling ' + page_url)
                print('Queue ' + str(len(Crawler.queue)) + ' | Crawled  ' + str(len(Crawler.crawled)))
            links = Crawler.gather_links(page_url)
            Crawler.add_links_to_queue(links)
            Crawler.crawled.add(page_url)

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        url_info = urllib.request.urlparse(page_url)
        if url_info.netloc != Crawler.domain_name:
            return set()
        try:
            response = urllib.request.urlopen(page_url)
        except:
            print("Cannot open page: " + page_url)
            return set()
        if 'text/html' in response.getheader('Content-Type'):
            html_bytes = response.read()
            soup = bs4.BeautifulSoup(html_bytes, "html.parser")
            if config.GENERATE_SITE_MAP:
                path = url_info.path
                Crawler.xml_writer.write(path)
            if config.DOWNLOAD_HTML:
                file_path = file_writing.get_file_path(Crawler.project_name, page_url)
                file_writing.create_dir_from_file_path(file_path)
                try:
                    html_string = html_bytes.decode("utf-8")
                    file_writing.write_file(file_path, html_string)
                except:
                    print("Cannot write to file: " + page_url)
            scraping.scrape(soup, Crawler.domain_name, Crawler.xml_writer)
            return scraping.get_links(soup, Crawler.base_url)

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

