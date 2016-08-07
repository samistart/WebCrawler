import os
from config import *
import urllib.request
import threading


def get_file_path(project_name, page_url):
    path = urllib.request.urlparse(page_url).path
    if path.endswith("/"):  #todo use os independent file seperators
        path = path[:-1]
    if '.' not in path:
        path += ".html"
    return project_name + path


def get_file_location(file_path):
    result = ""
    if '/' in file_path:
        k = file_path.rfind("/")    #todo use os independent file seperators
        result = file_path[:k]
    return result


def create_dir_from_file_path(file_path):
    file_location = get_file_location(file_path)
    if not file_location == "" and not os.path.exists(file_location):
        os.makedirs(file_location)


def create_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


def asynchronous_url_retrieve(location, file_path):
    def target():
        urllib.request.urlretrieve(location, file_path)
    t = threading.Thread(target=target)
    t.start()
