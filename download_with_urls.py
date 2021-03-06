# -*- coding: utf-8 -*-
# @Author:              Chris Eugene Mills
# @Date:                2021-01-12
# @Last Modified by:    Chris Eugene Mills
# @Last Modified time:  2021-01-12


####################################################################################################################
# Download images from google with predefined urls
# Use selenium and urllib, and each search query will download any number of images that google provide
# allow single process or multiple processes for downloading
# Pay attention that since selenium is used, geckodriver and firefox browser is required
####################################################################################################################


import os
import time
# from multiprocessing import Pool

from googleimagesdownloader.processes import get_image_links_from_raw_url, download_link_list_file
from googleimagesdownloader.utils import get_query_from_google_url

from googleimagesdownloader.config import establish_operating_dirs

config = {
    "download_dir": './data/',
    "link_files_dir": './data/link_files/',
    "log_dir": './logs/',
    "count": 15,
    "urls": [
        'https://www.google.com/search?q=site:www.archdaily.com&tbm=isch&hl=en&tbs=rimg:CY6BaeP57DUSYQS4KfegE227&sa=X&ved=0CAIQrnZqFwoTCJjl0_C8le4CFQAAAAAdAAAAABAT#imgrc=Ty9ETuBZ8xcZLM',
        ],
}

def main():

    ###################################
    # get image links and store in file
    ###################################
    # single process
    for url in config['urls']:
        label = get_query_from_google_url(url)
        if not label:
            continue
        get_image_links_from_raw_url(url, config['link_files_dir'] + label, config['count'])
    

    # multiple processes
    # p = Pool(3) # default number of process is the number of cores of your CPU, change it by yourself
    # for url in config['urls']:
    #     label = get_query_from_google_url(url)
    #     if not label:
    #         continue
    #     p.apply_async(get_image_links_from_raw_url, args=(url, config['link_files_dir'] + label, config['count']))
    # p.close()
    # p.join()
    print('Finish getting all image links')

    ###################################

    time.sleep(5)
    
    ###################################
    # download images with link file
    ###################################
    # single process
    for url in config['urls']:
        label = get_query_from_google_url(url)
        if not label:
            continue
        download_link_list_file(config['link_files_dir'] + label, config['download_dir'], config['log_dir'])
    
    # multiple processes
    # p = Pool() # default number of process is the number of cores of your CPU, change it by yourself
    # for url in config['urls']:
    #     label = get_query_from_google_url(url)
    #     if not label:
    #         continue
    #     p.apply_async(download_link_list_file, args=(config['link_files_dir'] + label, config['download_dir'], config['log_dir']))
    # p.close()
    # p.join()
    print('Finish downloading all images')


if __name__ == "__main__":
    establish_operating_dirs(config)
    main()
