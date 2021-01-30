import os
import pathvalidate

from .processes import (
    process_google_url,
    download_link_list
)

from .utils import (
    get_query_from_google_url, 
    get_shortcode_id, 
    get_timestamp_str,
    write_url_list
)


class Job:
    def __init__(self, config, index = 0):
        # Ingest global config settings
        # TODO cast config to explicit args
        # TODO validate config
        self.config = config.copy()

        self.url = ""
        self.id = ""
        self.dir = ""
        self.results = []

        pages = self.config.get('pages', [])
        if len(pages):
            i = max(0, min(index, len(pages)-1))
            self.set_page_from_url(pages[i])

        # TODO if len(keywords)....


    def set_page_from_url(self, url):
        # TODO validate url
        self.url = url
        self.__generate_job_id()
        self.__set_job_dir()


    def set_page_from_keyword(self, key):
        # TODO implement
        pass


    def scan_page(self, write = False):
        if not self.url:
            return
        num_skip = self.config.get('skip', 0)
        num_requested = self.config.get('count', 100)
        img_urls = process_google_url(self.url, num_skip, num_skip + num_requested)
        if not img_urls:
            return
        self.results = list( set(self.results) | set(img_urls) )

        if write:
            self.write_links_file()


    def write_links_file(self):
        if not self.url or not self.results or not self.dir:
            return
        link_file_path = os.path.join( self.dir, "links.txt" )
        write_url_list( link_file_path, self.results )


    def download(self):
        if not self.url or not self.results or not self.dir:
            return
        download_link_list( self.results, self.dir )


    # PRIVATE #####################################################################

    def __generate_job_id(self):
        query = get_query_from_google_url(self.url)
        query = 'untitled' if query is None else query
        scode = get_shortcode_id(self.url)
        times = get_timestamp_str()
        id = f"{times}_{query}_{scode}"
        id = id.replace(' ', '-')
        id = pathvalidate.sanitize_filename(id)
        self.id = id
        print(f'Job ID: {self.id}')

    def __set_job_dir(self):
        # TODO check for download_dir key
        # TODO check for self.id existence
        self.dir = os.path.join( self.config["download_dir"], self.id, "" )
        print(f"Output: {self.dir}")



