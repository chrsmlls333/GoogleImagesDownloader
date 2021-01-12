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