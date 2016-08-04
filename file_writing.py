import os
from config import *
from urllib.request import urlparse


def get_file_path(project_name, page_url):
    path = urlparse(page_url).path
    if path.endswith("/"):  #todo use os independent file seperators
        path = path[:-1]
    if '.' not in path:
        path += ".html"
    return project_name + path


def get_file_location(file_path):
    if '/' in file_path:
        k = file_path.rfind("/")    #todo use os independent file seperators
        return file_path[:k]
    else:
        return ""


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
