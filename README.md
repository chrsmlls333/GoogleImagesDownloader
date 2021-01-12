# GoogleImagesDownloader

This repository can download images from google with specified keywords

## Requirements

- python 3.6
- selenium 3.6.0
- Firefox
- geckodriver

**Firefox and geckodriver are required by selenium, and Firefox 55 or greater is recommended, cause [geckodriver][1] support that best. As for geckodriver, just download the latest version of geckodriver from [here][2], then add it to the PATH environment variable.**

Here is an example of downloading with selenium using 2 processes

<img src="/imgs/download_with_selenium.gif?raw=true">

## Details and Configuration

### Two Methods

Two different methods are provided

- `other/download_with_urllib`
- `download_with_keywords` (with Selenium)
- `download_with_urls` (with Selenium)


`download_with_urllib` is to download with just package `urllib`, but due to the limit by google, each searching query can download at most 100 images

The rest of the scripts in root download with package `selenium` and `urllib`. With selenium, we can directly search and scroll in the browser, so we can get more than 100 images for each searching query.

**Both of the above methods support downloading with single process or mulitple processes**, and `download_with_keywords` will firstly store the actual links of images in a file, then download the actual images with the file, while `download_with_urllib` will directly download all the images since the number if small

**Specify `main_keywords` and `supplemented_keywords` in the code**, each `main_keyword` will join with each `supplemented_keyword` to become a searching query, and one directory will be created for each main_keyword to store the related images. The following image is a simple example 

<img src="/imgs/keywords.png?raw=true">


[1]: https://github.com/mozilla/geckodriver
[2]: https://github.com/mozilla/geckodriver/releases
[3]: https://github.com//WuLC/GoogleImagesDownloader/blob/master/imgs/download_with_selenium.gif
[4]: http://static.zybuluo.com/WuLiangchao/pcnc2a7dge8y2jh0lt15l05l/image_1c52u2p8r1t8hfkmsie10lr1d1qm.png