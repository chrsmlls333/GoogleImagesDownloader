# -*- coding: utf-8 -*-
# @Author:              Chris Eugene Mills
# @Date:                2021-01-12
# @Last Modified by:    Chris Eugene Mills
# @Last Modified time:  2021-01-19


####################################################################################################################
# Download images from google with predefined urls
# Use selenium and urllib, and each search query will download any number of images that google provide
# allow single process or multiple processes for downloading
# Pay attention that since selenium is used, geckodriver and firefox browser is required
####################################################################################################################


import os
import time
# from multiprocessing import Pool

from googleimagesdownloader.processes import process_google_url, download_link_list
from googleimagesdownloader.utils import generate_job_id, write_url_list, read_url_list
from googleimagesdownloader.config import establish_operating_dirs

config = {
    "download_dir": './data/',
    "link_files_dir": './data/link_files/',
    "log_dir": './logs/',
    "count": 15,
    "skip": 0,
    "pages": [
        'https://www.google.com/search?q=site:www.archdaily.com&tbm=isch&hl=en&tbs=rimg:CY6BaeP57DUSYQS4KfegE227&sa=X&ved=0CAIQrnZqFwoTCJjl0_C8le4CFQAAAAAdAAAAABAT#imgrc=Ty9ETuBZ8xcZLM',
        ],
}

def main():

    jobs = []
    
    # single process loop
    for page in config['pages']:

        # Build Job 
        job = config.copy()
        job.pop('pages', None)
        job_id = generate_job_id(page)
        job_dir = os.path.join(job["download_dir"], job_id, "")
        job.update({
            "page": page,
            "job_id": job_id,
            "job_dir": job_dir,
            "links": [],
        })
        print(f'Job ID: {job["job_id"]}')

        # Get Image Links
        num_skip = job.get('skip', 0)
        num_requested = job.get('count', 100)
        img_urls = process_google_url(page, num_skip, num_skip + num_requested)
        if not img_urls:
            continue
        job.update({ "links": img_urls })

        # Write Links to File
        link_file_path = os.path.join(job['job_dir'], "links.txt")
        write_url_list(link_file_path, img_urls)

        # Save Job
        jobs.append(job)

    # multiple processes
    # p = Pool(3) # default number of process is the number of cores of your CPU, change it by yourself
    # for url in config['urls']:
    #     p.apply_async(get_image_links_from_raw_url, args=(config, url))
    # p.close()
    # p.join()
    print('Finish getting all image links')


    ###################################
    time.sleep(5)
    ###################################


    # single process
    for job in jobs:

        # Download Images with Link List saved to Job
        download_link_list(job['links'], job['job_dir'])

        # TODO write job config json to job_dir
    
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
    # TODO conform config here
    establish_operating_dirs(config)
    main()
