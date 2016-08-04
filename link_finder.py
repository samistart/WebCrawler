from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse


class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attr, value) in attrs:
                if attr == 'href':
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)

    def get_page_links(self):
        return self.links

    def error(self, message):
        pass
