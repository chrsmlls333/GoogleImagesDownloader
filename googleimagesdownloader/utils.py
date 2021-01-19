from mimetypes import init, types_map
init()
def get_extensions_for_type(general_type):
    for ext in types_map:
        if types_map[ext].split('/')[0] == general_type:
            yield ext

from re import findall
from pathvalidate import sanitize_filename
def get_query_from_google_url(url):
    query = findall('[?&]q=([^&]+)', url)
    if not query:
        return None
    return sanitize_filename(query[0], replacement_text='_')

from hashlib import sha1
def get_shortcode_id(s):
    assert isinstance(s, str), "get_shortcode_id: must be provided a string."
    return sha1(s.encode('utf-8')).hexdigest()[0:7]