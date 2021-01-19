
import os
import time
import datetime
import math
import re
import pathvalidate
import hashlib
import mimetypes
mimetypes.init()
from urllib.parse import urlparse


# STRING / PATH OPS #########################################

def zeropad(num, maximum = 100):
    return str(num).zfill(math.floor(math.log10(maximum)+1))


def get_extensions_for_type(general_type):
    for ext in mimetypes.types_map:
        if mimetypes.types_map[ext].split('/')[0] == general_type:
            yield ext


def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


def get_query_from_google_url(url):
    query = re.findall('[?&]q=([^&]+)', url)
    if not query:
        return None
    return pathvalidate.sanitize_filename(query[0], replacement_text='')


def get_shortcode_id(s):
    assert isinstance(s, str), "get_shortcode_id: must be provided a string."
    return hashlib.sha1(s.encode('utf-8')).hexdigest()[0:7]


def get_timestamp_str():
    now = datetime.datetime.now()
    return now.strftime("%y%m%d%H%M%S")


def generate_job_id(url):
    query = get_query_from_google_url(url)
    query = 'untitled' if query is None else query
    scode = get_shortcode_id(url)
    times = get_timestamp_str()
    id = f"{times}_{query}_{scode}"
    id = id.replace(' ', '-')
    id = pathvalidate.sanitize_filename(id)
    return id

# FILE OPERATIONS ############################################

def write_url_list(path, text_set):
    """write list of strings to file as lines
    
    Args:
        path (str): local file path
        text_set (set[str]): list of strings to write
    
    Returns:
        path (str): sanitized local file path
    """
    assert isinstance(text_set, (tuple, list, set)), "write_url_list: text_set is not an iterable."
    assert isinstance(path, str), "write_url_list: path is not a string." 

    path = pathvalidate.sanitize_filepath(path, platform='universal')

    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, 'w') as wf:
        for s in text_set:
            wf.write(s +'\n')

    return path


def read_url_list(path):
    """read file to list of strings, validate urls
    
    Args:
        path (str): local file path
    
    Returns:
        urls (set[str]): list of unique, validated urls
    """

    assert isinstance(path, str), "read_url_list: path is not a string." 
    assert os.path.exists(path), "read_url_list: url list at path doesn't exist."

    with open(path) as rf:
        content = rf.read().splitlines()
    content = set(content)
    print(len(content))

    content = filter(lambda url: validate_url(url), content)
    print(len(content))

    return content
    
