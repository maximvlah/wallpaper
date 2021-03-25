import os
import time
import ntpath
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
import random


def scrape(category,resolution,page_number=10):

    '''
        Download wallpapers from the wallpaperscraft.com based on the given resolution and category

        Attributes:
            category: str (ex: 'nature'; see all the categories on wallpaperscraft.com)
            resolution: str; your screen resolution in format 'widthxheight'
            page_number: int; how many images you want download (there's 15-16 images per page, so page_number 10 = 160 images)
              -> the pages are picked randomly
    '''

    #open browser
    driver = webdriver.Firefox()

    #get total number of pages of this category
    driver.get(f'https://wallpaperscraft.com/catalog/{category}/{resolution}/page1')
    #go to last page
    driver.find_element_by_class_name('pager__item_last-page').click()
    #retrieve the total number of pages for the category
    total_num_pages = int(ntpath.basename(driver.current_url).replace('page',''))
    #generate random set of numbers within that range
    n = random.sample(range(1,total_num_pages), page_number)

    print('Downloading images')
    time.sleep(1)
    
    for p in tqdm(n): 
        #get url
        url = f'https://wallpaperscraft.com/catalog/{category}/{resolution}/page{p}'
        driver.get(url)

        #get link of each image on the page
        img_links = driver.find_elements_by_class_name("wallpapers__link")
        links = [elem.get_attribute('href') for elem in img_links]

        #download images from each link one after another
        for link in links:

            driver.get(link)
            #click on a link
            driver.find_element_by_link_text(f'Download wallpaper {resolution}').click()

            # get the image source
            img = driver.find_element_by_tag_name('img')
            src = img.get_attribute('src') 

            # download the image
            urllib.request.urlretrieve(src, f'photos/{ntpath.basename(src)}')
    driver.close()

def main():
    category = 'nature'
    resolution = '1920x1080'
    scrape(category,resolution,10)

if __name__ == '__main__':
    main()