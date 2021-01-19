# -*- coding: utf-8 -*-
# @Author:              WuLC
# @Date:                2017-09-27 23:02:19
# @Last Modified by:    Chris Eugene Mills
# @Last Modified time:  2021-01-09


####################################################################################################################
# Download images from google with specified keywords for searching
# search query is created by "main_keyword + supplemented_keyword"
# if there are multiple keywords, each main_keyword will join with each supplemented_keyword
# Use selenium and urllib, and each search query will download any number of images that google provide
# allow single process or multiple processes for downloading
# Pay attention that since selenium is used, geckodriver and firefox browser is required
####################################################################################################################


import os
import time
from multiprocessing import Pool

from googleimagesdownloader.processes import get_image_links_from_keywords, download_link_list_file

from googleimagesdownloader.config import establish_operating_dirs

config = {
    "download_dir": './data/',
    "link_files_dir": './data/link_files/',
    "log_dir": './logs/',
    "count": 100,
    "main_keywords": ['floorplans'],
    "supplemented_keywords": ['', 'b+w', 'mies van der rohe'],

    # "supplemented_keywords": ['facial expression',\
    #             'human face',\
    #             'face',\
    #             'old face',\
    #             'young face',\
    #             'adult face',\
    #             'child face',\
    #             'woman face',\
    #             'man face',\
    #             'male face',\
    #             'female face',\
    #             'gentleman face',\
    #             'lady face',\
    #             'boy face',\
    #             'girl face',\
    #             'American face',\
    #             'Chinese face',\
    #             'Korean face',\
    #             'Japanese face',\
    #             'actor face',\
    #             'actress face'\
    #             'doctor face',\
    #             'movie face'
    #             ],

    # test for chinese
    # "main_keywords": ['高兴', '悲伤', '惊讶'],
    # "supplemented_keywords": ['人脸'],

    # test for japanese
    # "main_keywords": ['喜びます', 'きょうがいする', '悲しみ'],
    # "supplemented_keywords": ['顔つき'],
}

def main():

    ###################################
    # get image links and store in file
    ###################################
    # single process
    # for keyword in config['main_keywords']:
    #     link_file_path = link_files_dir + keyword
    #     get_image_links_from_keywords(keyword, config['supplemented_keywords'], config['link_files_dir'] + keyword, config['count'])
    

    # multiple processes
    p = Pool(3) # default number of process is the number of cores of your CPU, change it by yourself
    for keyword in config['main_keywords']:
        p.apply_async(get_image_links_from_keywords, args=(keyword, config['supplemented_keywords'], config['link_files_dir'] + keyword, config['count']))
    p.close()
    p.join()
    print('Finish getting all image links')

    ###################################

    time.sleep(5)
    
    ###################################
    # download images with link file
    ###################################
    # single process
    # for keyword in config['main_keywords']:
    #     link_file_path = link_files_dir + keyword
    #     download_link_list_file(config['link_files_dir'] + keyword, config['download_dir'], config['log_dir'])
    
    # multiple processes
    p = Pool() # default number of process is the number of cores of your CPU, change it by yourself
    for keyword in config['main_keywords']:
        p.apply_async(download_link_list_file, args=(config['link_files_dir'] + keyword, config['download_dir'], config['log_dir']))
    p.close()
    p.join()
    print('Finish downloading all images')

if __name__ == "__main__":
    establish_operating_dirs(config)
    main()