import config
import file_writing
import urllib.parse
import urllib.request
import os

scraped = set()


def scrape(soup, domain_name, xml_writer):
    for asset in [i.get('src') for i in soup.find_all() if i.get('src')]:
        parse = urllib.parse.urlparse(asset)
        if parse.netloc == '' or parse.netloc == domain_name:
            path = parse.path
            url = urllib.parse.urljoin(config.BASE_URL, parse.path)
            if url not in scraped:
                if config.DOWNLOAD_ASSETS:
                    file_path = config.PROJECT_NAME + parse.path
                    file_writing.create_dir_from_file_path(file_path)
                    if not os.path.isfile(file_path):
                        file_writing.asynchronous_url_retrieve(url, file_path)
                if config.GENERATE_SITE_MAP:
                    xml_writer.write(path)
            scraped.add(path)


def get_links(soup, base_url):
    links = set()
    for a in soup.find_all('a', href=True):
        parse = urllib.parse.urlparse(a['href'])
        if parse.netloc == '' or parse.netloc == base_url:
            path = parse.path
            link = base_url + path
            links.add(link)
    return links




