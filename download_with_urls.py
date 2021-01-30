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
import multiprocessing as mp

from googleimagesdownloader.config import establish_operating_dirs
from googleimagesdownloader.Job import Job

config = {
    "download_dir": './data/',
    "link_files_dir": './data/link_files/',
    "log_dir": './logs/',
    "count": 5,
    "skip": 0,
    "concurrency": 2,
    "pages": [
        'https://www.google.com/search?q=site:www.archdaily.com&tbm=isch&hl=en&tbs=rimg:CY6BaeP57DUSYQS4KfegE227&sa=X&ved=0CAIQrnZqFwoTCJjl0_C8le4CFQAAAAAdAAAAABAT#imgrc=Ty9ETuBZ8xcZLM',
        'https://www.google.com/search?q=site%3Awww.archdaily.com&tbm=isch&ved=2ahUKEwjO98Hk1sTuAhWNFqwKHUBbChwQ2-cCegQIABAA&oq=site%3Awww.archdaily.com&gs_lcp=CgNpbWcQDFAAWABglzFoAHAAeACAAQCIAQCSAQCYAQCqAQtnd3Mtd2l6LWltZw&sclient=img&ei=7dkVYI7NH42tsAXAtqngAQ&hl=en',
        'https://www.google.com/search?q=site:www.archdaily.com&tbm=isch&hl=en&tbs=itp:lineart&sa=X&ved=0CAIQpwVqFwoTCNi99e_WxO4CFQAAAAAdAAAAABAC&biw=1903&bih=947',
        ],
}

def main():
    

    # initialize all
    jobs = []
    for i, _ in enumerate(config['pages']):
        job = Job(config, i)
        jobs.append(job)

    # multiple processes
    # default number of process is the number of cores of your CPU, change it by yourself
    with mp.Pool(config['concurrency']) as p:
        jobs = p.map(pool_scan_page, jobs)
        print('Finish getting all image links')
        time.sleep(3)
        jobs = p.map(pool_download, jobs)
        # TODO write job config json to job_dir
        print('Finish downloading all images')


def pool_scan_page(job):
    job.scan_page(write=True)
    return job

def pool_download(job):
    job.download()
    return job


if __name__ == "__main__":
    # TODO conform config here
    establish_operating_dirs(config)
    main()
