
import os
import time
import math
import logging

import urllib.request
import urllib.error
from urllib.parse import urlparse, quote

import mimetypes
mimetypes.init()

import pathvalidate

from user_agent import generate_user_agent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .utils import get_extensions_for_type



def process_google_url(url, index_start = 0, index_end = 1000):
    """get image links with selenium
    
    Args:
        url (str): google images url
        index_start (int):
        index_end (int):
    
    Returns:
        set[str]: a deduped set of image urls
    """
    # Check url for googliness
    pass

    # Check num_requested
    # TODO Check types
    num_requested = abs(index_end - index_start) 
    index_start = min(index_start, index_end)
    index_end = index_start + num_requested
    if index_end <= 0: 
        raise ValueError("process_google_url: 2nd arg cannot be 0. Nothing to get!")
    number_of_scrolls = int(index_end / 400) + 1 # number_of_scrolls * 400 images will be opened in the browser
    
    # Report
    print(f"process_google_url({url})")
    print(f"Requested {num_requested} images.")
    if index_start > 0:
        print(f"Skipping the first {index_start} images.")

    # Prepare
    img_urls = set()
    driver = webdriver.Firefox()

    # Open page and Scan
    driver.get(url)
    for _ in range(number_of_scrolls):
        for __ in range(10):
            # multiple scrolls needed to show all 400 images
            driver.execute_script("window.scrollBy(0, 1000000)")
            time.sleep(2)
        # to load next 400 images
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//input[@value='Show more results']").click()
        except Exception as e:
            print("Reached the end of page without 'Show more results' button.")
            break

    # imges = driver.find_elements_by_xpath('//div[@class="rg_meta"]') # not working anymore
    # imges = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]') # not working anymore
    thumbs = driver.find_elements_by_xpath('//a[@class="wXeWr islib nfEiy mM5pbd"]')
    print(f"Found {len(thumbs)} thumbnails.")

    num_found = 0
    for index, thumb in enumerate(thumbs):
        if (index < index_start): 
            continue 
        if num_found >= num_requested: 
            break 

        try:
            thumb.click()
            time.sleep(1)
        except e:
            print("Error clicking one thumbnail.")

        url_elements = driver.find_elements_by_xpath('//img[@class="n3VNCb"]')
        for url_element in url_elements:
            try:
                url = url_element.get_attribute('src')
            except e:
                print("Error getting one url.")

            if url.startswith('http') and not url.startswith('https://encrypted-tbn0.gstatic.com'):
                img_urls.add(url)

                num_found += 1
                num_found_leading = str(num_found).zfill(math.floor(math.log10(len(thumbs))+1))
                print(f"[{num_found_leading}] Found image url: " + url)

    print(f'Found {len(img_urls)} images.')
    driver.quit()

    # Return the goods
    return img_urls


def write_url_list(path, text_set):
    """write list of strings to file as lines
    
    Args:
        path (str): local file url
        text_set (set[str]): list of strings to write
    
    Returns:
        None
    """
    assert isinstance(text_set, (tuple, list, set)), "text_set is not an iterable."
    assert isinstance(path, str), "path is not a string." 

    path = pathvalidate.sanitize_filepath(path, platform='universal')

    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(path, 'w') as wf:
        for s in text_set:
            wf.write(s +'\n')


def get_image_links_from_keywords(main_keyword, supplemented_keywords, link_file_path, num_requested = 1000, num_skip = 0):
    """get image links with selenium
    
    Args:
        main_keyword (str): main keyword
        supplemented_keywords (list[str]): list of supplemented keywords
        link_file_path (str): path of the file to store the links
        num_requested (int, optional): maximum number of images to download
        num_skip (int, optional): first batch to skip
    
    Returns:
        None
    """

    # TODO typecheck args

    index_start = num_skip
    index_end = num_skip + num_requested

    print(f"Requested {num_requested} images.")
    if index_start > 0:
        print(f"Skipping the first {index_start} images.")

    img_urls = set()
    for i, sup_kw in enumerate(supplemented_keywords):
        search_query = quote((main_keyword + ' ' + sup_kw).strip())
        url = "https://www.google.com/search?q="+search_query+"&source=lnms&tbm=isch"
        # url = url + "&tbs=ic:gray" #black and white only

        img_urls |= process_google_url(url, index_start, index_end)

        print('get_image_links_from_keywords({0}, {1}) got {2} image urls so far.'.format(main_keyword, sup_kw, len(img_urls)))
    print('get_image_links_from_keywords({0}) found {1} images total.'.format(main_keyword, len(img_urls)))

    write_url_list(link_file_path, img_urls)
    print('Store all the links in file {0}'.format(link_file_path))


def get_image_links_from_raw_url(url, link_file_path, num_requested = 1000, num_skip = 0):
    """get image links with selenium
    
    Args:
        url (str): main path to image gallery
        link_file_path (str): path of the file to store the links
        num_requested (int, optional): maximum number of images to download
        num_skip (int, optional): first batch to skip
    
    Returns:
        None
    """

    # TODO typecheck args

    index_start = num_skip
    index_end = num_skip + num_requested

    print(f"Requested {num_requested} images.")
    if index_start > 0:
        print(f"Skipping the first {index_start} images.")

    img_urls = process_google_url(url, index_start, index_end)

    print(f'get_image_links_from_raw_url({url}) found {len(img_urls)} images total.')

    write_url_list(link_file_path, img_urls)
    print('Store all the links in file {link_file_path}')


def download_link_list_file(link_file_path, download_dir, log_dir):
    """download images whose links are in the link file
    
    Args:
        link_file_path (str): path of file containing links of images
        download_dir (str): directory to store the downloaded images
    
    Returns:
        None
    """
    print('Start downloading with link file {0}..........'.format(link_file_path))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    main_keyword = link_file_path.split('/')[-1]
    log_file = log_dir + 'download_selenium_{0}.log'.format(main_keyword)
    logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode="a+", format="%(asctime)-15s %(levelname)-8s  %(message)s")
    img_dir = download_dir + main_keyword + '/'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    # start to download images
    with open(link_file_path, 'r') as rf:
        for index, link in enumerate(rf):
            link = link.strip()

            print(' ')
            success = download_image_link(link, img_dir, f'{index+1}_')
            if not success:
                continue

            # Breathe
            if (index+1) % 10 == 0:
                print('\nProcess-{0} is sleeping...'.format(main_keyword))
                time.sleep(5)

def download_image_link(link, dir_path, prefix = ''):
    """Use urllib to download asset
    
    Args:
        link (str):
        dir_path (str):
        prefix (str):
    
    Returns:
        bool
    """
    print(f'download_image_link: from "{link}"')

    try:
        o = urlparse(link)
        ref = o.scheme + '://' + o.hostname
        #ref = 'https://www.google.com'
        ua = generate_user_agent()
        headers = {}
        headers['User-Agent'] = ua
        headers['referer'] = ref
        # print(f'\n{link}\n{ref}\n{ua}')
        req = urllib.request.Request(link, headers = headers)
        response = urllib.request.urlopen(req)
        info = response.info()
        data = response.read()

        file_name_orig = (os.path.basename(o.path))
        file_name_orig_root, file_name_orig_ext = os.path.splitext(file_name_orig)
        img_exts = tuple(get_extensions_for_type('image'))
        ext_suggest = mimetypes.guess_extension(info.get_content_type())
        if file_name_orig_ext.strip() and file_name_orig_ext.lower() in img_exts:
            file_name = file_name_orig
        else:
            if not ext_suggest.strip():
                raise Exception("Found and guessed extensions not adequate... not an image?")
            file_name = file_name_orig_root + ext_suggest
            print(f"{file_name_orig_ext} -> {ext_suggest}")
        
        file_name = prefix + file_name
        file_path = dir_path + file_name

        with open(file_path,'wb') as wf:
            wf.write(data)

        print(f'download_image_link: to "{file_name}"')
        return True

    except urllib.error.URLError as e:
        print('URLError')
        logging.error('URLError while downloading image {0}reason:{1}'.format(link, e.reason))
        return False
    except urllib.error.HTTPError as e:
        print('HTTPError')
        logging.error('HTTPError while downloading image {0}http code {1}, reason:{2}'.format(link, e.code, e.reason))
        return False
    except Exception as e:
        print('Unexpected Error')
        logging.error('Unexpected error while downloading image {0}error type:{1}, args:{2}'.format(link, type(e), e.args))
        return False